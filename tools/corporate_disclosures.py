from pdf2image import convert_from_path
from pathlib import Path
from smolagents import tool
import os
from playwright.sync_api import sync_playwright
import time
from typing import List
from PIL import Image
from tools.image_analysis import read_images
import gc

def get_pdf_page_count(pdf_path):
    """
    Get the total number of pages in a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        int: Total number of pages in the PDF, or None if unable to determine
    """
    try:
        # Try using PyPDF2 if available
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(pdf_path)
            return len(reader.pages)
        except ImportError:
            # If PyPDF2 is not available, try alternative method
            try:
                import fitz  # PyMuPDF
                doc = fitz.open(pdf_path)
                page_count = len(doc)
                doc.close()
                return page_count
            except ImportError:
                # Fallback: estimate by trying to process pages incrementally
                return None
    except Exception as e:
        print(f"Warning: Could not determine page count for {pdf_path}: {e}")
        return None

def create_images_from_pdfs(downloaded_pdfs, chunk_size=5):
    """
    Convert PDF files to images, processing in chunks to reduce memory usage.
    
    This function processes PDFs page by page or in small batches to prevent
    memory errors on small machines. Each chunk is processed and freed before
    moving to the next.
    
    Args:
        downloaded_pdfs (list): List of paths to PDF files to process
        chunk_size (int): Number of pages to process at once (default: 5)
                         Smaller values use less memory but may be slower
        
    Returns:
        list: List of PIL Image objects extracted from all PDFs
    """
    information_array = []
    
    for pdf_path in downloaded_pdfs:
        try:
            print(f"Processing PDF: {pdf_path}")
            
            # Get total page count if possible
            total_pages = get_pdf_page_count(pdf_path)
            processed_successfully = False
            
            if total_pages is None:
                # Try to process all pages at once first (for small PDFs)
                # If this fails with MemoryError, fall back to chunked processing
                print(f"Page count unknown, attempting to process all pages at once for {pdf_path}")
                try:
                    images = convert_from_path(pdf_path, dpi=200)
                    for image in images:
                        information_array.append(image)
                        print(f"Converted {pdf_path} to image")
                    # Free memory
                    del images
                    gc.collect()
                    processed_successfully = True
                except MemoryError as e:
                    print(f"Memory error processing {pdf_path}: {e}")
                    print("Falling back to incremental chunked processing...")
                    processed_successfully = False
                except Exception as e:
                    print(f"Error processing {pdf_path}: {e}")
                    processed_successfully = False
            
            if not processed_successfully:
                if total_pages is not None:
                    # Process PDF in chunks with known page count
                    print(f"Processing {total_pages} pages in chunks of {chunk_size}")
                    
                    for start_page in range(1, total_pages + 1, chunk_size):
                        end_page = min(start_page + chunk_size - 1, total_pages)
                        print(f"Processing pages {start_page}-{end_page} of {total_pages}")
                        
                        try:
                            # Convert chunk of pages
                            chunk_images = convert_from_path(
                                pdf_path,
                                dpi=200,
                                first_page=start_page,
                                last_page=end_page
                            )
                            
                            # Add images to result array
                            for image in chunk_images:
                                information_array.append(image)
                                print(f"Converted page from {pdf_path} to image")
                            
                            # Free memory immediately after processing chunk
                            del chunk_images
                            gc.collect()
                            
                        except Exception as e:
                            print(f"Error processing pages {start_page}-{end_page} of {pdf_path}: {e}")
                            continue
                else:
                    # Incremental approach: try processing small chunks until we get an error
                    print(f"Using incremental chunked processing for {pdf_path}")
                    current_page = 1
                    
                    while True:
                        try:
                            # Try to process next chunk
                            chunk_images = convert_from_path(
                                pdf_path,
                                dpi=200,
                                first_page=current_page,
                                last_page=current_page + chunk_size - 1
                            )
                            
                            if not chunk_images:
                                # No more pages
                                break
                            
                            # Add images to result array
                            for image in chunk_images:
                                information_array.append(image)
                                print(f"Converted page from {pdf_path} to image")
                            
                            # Free memory
                            del chunk_images
                            gc.collect()
                            
                            # Move to next chunk
                            current_page += chunk_size
                            
                        except Exception as e:
                            # Likely reached end of PDF or error
                            if current_page == 1:
                                # Error on first chunk, this PDF might be corrupted
                                print(f"Failed to process first chunk of {pdf_path}: {e}")
                            break

        except Exception as e:
            print(f"Error processing PDF {pdf_path}: {e}")
            continue
        
        # Force garbage collection after each PDF
        gc.collect()
    
    print(f"Successfully extracted information from {len(information_array)} images across {len(downloaded_pdfs)} PDFs")
    
    return information_array


def get_downloaded_pdfs(url,row_identifier) -> list:
    """
    Download PDF files from the specified URL and return their paths.
    
    Args:
        url (str): The URL to scrape for PDF links.
        row_identifier (str): CSS selector to identify rows containing PDF links.
        ticker (str): Stock ticker/symbol to append to downloaded file names.
    
    Returns:
        list: A list of paths to the downloaded PDF files.
    """
    # Array to store downloaded PDF locations
    downloaded_pdfs = []
    
    try:
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            
            # Navigate to the URL
            print(f"Navigating to: {url}")
            page.goto(url, wait_until="networkidle",timeout=60000)
            
            # Wait for page to load completely
            page.wait_for_load_state("networkidle")
            time.sleep(10)  # Additional wait to ensure dynamic content loads
            
            # Click on the "Corporate Disclosures" span element
            try:
                # Look for the Corporate Disclosures element within the specified structure
                director_dealings_selector = "li label span:has-text('Corporate Disclosures')"
                page.wait_for_selector(director_dealings_selector, timeout=60000)
                page.click(director_dealings_selector)
                print("Successfully clicked on Corporate Dealings")
                time.sleep(3)  # Wait for the content to load after clicking
            except Exception as e:
                print(f"Could not find Corporate Disclosures element: {e}")
                # Try alternative selectors
                alternative_selectors = [
                    "span:has-text('Corporate Disclosures')",
                    "label:has-text('Corporate Disclosures')",
                    "li:has-text('Corporate Disclosures')"
                ]
                clicked = False
                for selector in alternative_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.click(selector)
                            print(f"Clicked using alternative selector: {selector}")
                            clicked = True
                            time.sleep(3)
                            break
                    except:
                        continue
                
                if not clicked:
                    print("Could not find Corporate Disclosures element with any selector")
                    browser.close()
                    return []
            
            # Create a temporary directory for downloads
            temp_dir = Path(__file__).resolve().parent.parent
            # with Path(__file__).resolve().parent.parent.parent as temp_dir:
            # Set up download behavior
            page.context.set_default_timeout(30000)
            
            # Collect all PDF links first before downloading (chunked approach)
            pdf_link_elements = []
            
            def collect_pdf_links():
                """Collect all PDF link elements from current page"""
                page_links = []
                
                # Process rows to collect links
                try:
                    rows = page.locator(row_identifier)
                    rows_count = rows.count()
                    print(f"Found {rows_count} rows")
                    
                    for i in range(rows_count):
                        row = rows.nth(i)
                        pdf_links = row.locator("td a[href*='.pdf']")
                        link_count = pdf_links.count()
                        
                        for j in range(link_count):
                            link = pdf_links.nth(j)
                            href = link.get_attribute("href")
                            if href and href.endswith('.pdf'):
                                page_links.append((link, f"{i}_{j}"))
                                
                except Exception as e:
                    print(f"Error collecting links from rows: {e}")
                
                # Alternative approach: look for all PDF links in the table
                if not page_links:
                    print("Trying alternative approach to find PDF links")
                    try:
                        all_pdf_links = page.locator("tbody#corpDisclose a[href*='.pdf']")
                        link_count = all_pdf_links.count()
                        print(f"Found {link_count} PDF links using alternative selector")
                        
                        for i in range(link_count):
                            link = all_pdf_links.nth(i)
                            href = link.get_attribute("href")
                            if href and href.endswith('.pdf'):
                                page_links.append((link, f"alt_{i}"))
                                
                    except Exception as e:
                        print(f"Error with alternative approach: {e}")
                
                return page_links
            
            # Function to download PDF from a link element
            def download_pdf_from_link(link_element, index):
                try:
                    href = link_element.get_attribute("href")
                    if href and href.endswith('.pdf'):
                        # Get the filename from the href
                        filename = href.split('/')[-1]
                        if not filename.endswith('.pdf'):
                            filename += '.pdf'
                        
                        # Create full path for the download
                        download_path = os.path.join(temp_dir, "downloads", f"{index}_{filename}")
                        
                        # Download the PDF
                        with page.expect_download() as download_info:
                            link_element.click()
                        
                        download = download_info.value
                        download.save_as(download_path)
                        
                        print(f"Downloaded PDF: {download_path}")
                        downloaded_pdfs.append(download_path)
                        
                except Exception as e:
                    print(f"Error downloading PDF: {e}")
            
            # Collect links from first page
            pdf_link_elements.extend(collect_pdf_links())
            
            # Handle pagination - navigate through all pages
            print("Starting pagination handling...")
            page_number = 1
            
            while True:
                print(f"Processing page {page_number}")
                
                # Check if there's a next page button
                try:
                    # Find the current page button
                    current_page = page.locator("#latestdisclosures_paginate  span a.paginate_button.current")
                    if current_page.count() == 0:
                        print("No pagination found or already on first page")
                        break
                    
                    # Find all pagination buttons
                    pagination_buttons = page.locator("#latestdisclosures_paginate  span a")
                    button_count = pagination_buttons.count()
                    
                    if button_count <= 1:
                        print("Only one page or no pagination buttons found")
                        break
                    
                    # Find the next page button (the one after current)
                    current_index = -1
                    for i in range(button_count):
                        button = pagination_buttons.nth(i)
                        if "current" in button.get_attribute("class") or "current" in button.get_attribute("className"):
                            current_index = i
                            break
                    
                    if current_index == -1:
                        print("Could not find current page button")
                        break
                    
                    # Check if there's a next page
                    if current_index >= button_count - 1:
                        print("Already on the last page")
                        break
                    
                    # Click on the next page button
                    next_button = pagination_buttons.nth(current_index + 1)
                    next_button.click()
                    print(f"Clicked on next page button (index {current_index + 1})")
                    
                    # Wait for the page to load
                    page.wait_for_load_state("networkidle")
                    time.sleep(3)  # Additional wait for content to load
                    
                    # Collect links from new page (don't download yet)
                    page_links = collect_pdf_links()
                    if page_links:
                        # Update indices for pagination
                        updated_links = [(link, f"page{page_number + 1}_{idx}") for link, idx in page_links]
                        pdf_link_elements.extend(updated_links)
                    
                    page_number += 1
                    
                except Exception as e:
                    print(f"Error handling pagination on page {page_number}: {e}")
                    break
            
            # Now download all collected PDFs in chunks of 10
            total_links = len(pdf_link_elements)
            print(f"Total PDF links collected: {total_links}")
            print(f"Starting chunked download (chunks of 10)...")
            
            download_chunk_size = 10
            for chunk_start in range(0, total_links, download_chunk_size):
                chunk_end = min(chunk_start + download_chunk_size, total_links)
                chunk = pdf_link_elements[chunk_start:chunk_end]
                
                print(f"Downloading chunk {chunk_start // download_chunk_size + 1} ({len(chunk)} PDFs: {chunk_start + 1}-{chunk_end} of {total_links})")
                
                for link_element, index in chunk:
                    download_pdf_from_link(link_element, index)
                    time.sleep(0.5)  # Small delay between downloads
                
                # Longer delay between chunks to avoid overwhelming the system
                if chunk_end < total_links:
                    print(f"Chunk completed. Waiting before next chunk...")
                    time.sleep(2)
        
            browser.close()
            
    except Exception as e:
        print(f"Error in web automation: {e}")
        return []
    
    print(f"Successfully downloaded {len(downloaded_pdfs)} PDFs")
    
    return downloaded_pdfs


tries = 0

@tool
def extract_corporate_disclosures(ticker:str,stock_exchange:str="NGX") -> List:
    """
    Extract corporate disclosure information from NGX (Nigerian Stock Exchange) company profiles.
    
    This function performs comprehensive web automation to download and convert 
    corporate disclosure PDFs from the NGX website to images
    
    Args:
        ticker (str): The stock ticker/symbol of the company (e.g., "ABCTRANS")
        stock_exchange (str): The stock exchange where the stock is listed. 
                             Currently only supports "NGX" (Nigerian Stock Exchange)
    
    Returns:
        list: A list of dictionaries containing the text content of each image in 
        3 categories namely text_ocr, text_easyocr, text_advanced   

    Example:
        extract_corporate_disclosures("ABCTRANS") ->  [
           {
           "text_ocr": "This is a test",
           "text_easyocr": "This is a test",
           "text_advanced": "This is a test"
           }
        ]
    
    Raises:
        ValueError: If stock_exchange is not "NGX" (currently only NGX is supported)
    
    Note:
        This function is specifically designed for NGX (Nigerian Stock Exchange) and requires
        the target company to have director disclosure information available on the NGX website.
        The function handles dynamic content loading and various table structures within PDFs.
    """

    if not stock_exchange == "NGX":

        return "The function can only work for ngx listed stocks"

    url = f"https://ngxgroup.com/exchange/data/company-profile/?symbol={ticker}&directory=companydirectory"
    row_identifier = "div#latestdisclosures table tbody tr"

    downloaded_pdfs = get_downloaded_pdfs(url, row_identifier)

    images_array = create_images_from_pdfs(downloaded_pdfs)
    text_content = read_images(images_array)

    global tries
    # Delete all downloaded PDFs after extracting information
    print("Cleaning up downloaded PDFs...")
    for pdf_path in downloaded_pdfs:
        try:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
                print(f"Deleted PDF: {pdf_path}")
            else:
                print(f"PDF not found for deletion: {pdf_path}")
        except Exception as e:
            print(f"Error deleting PDF {pdf_path}: {e}")
    
    print(f"Cleanup completed. Deleted {len(downloaded_pdfs)} PDF files.")

    if len(images_array) == 0 and tries < 2:
        print("No information extracted from PDFs.Will rerun once more")
        tries += 1
        return extract_corporate_disclosures(ticker, stock_exchange)

    return text_content
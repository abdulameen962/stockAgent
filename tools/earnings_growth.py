from smolagents import tool
import time
from typing import Dict
from playwright.sync_api import sync_playwright
from typing import Any
from tools.corporate_disclosures import create_images_from_pdfs
from tools.image_analysis import read_images
import os
from pathlib import Path

financial_statements = [

]

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
            
            # Click on the "Financials Statements" span element
            try:
                # Look for the Financials Statements element within the specified structure
                director_dealings_selector = "li label span:has-text('Financials Statements')"
                page.wait_for_selector(director_dealings_selector, timeout=60000)
                page.click(director_dealings_selector)
                print("Successfully clicked on Financials Statements")
                time.sleep(3)  # Wait for the content to load after clicking
            except Exception as e:
                print(f"Could not find Financials Statements element: {e}")
                # Try alternative selectors
                alternative_selectors = [
                    "span:has-text('Financials Statements')",
                    "label:has-text('Financials Statements')",
                    "li:has-text('Financials Statements')"
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
                    print("Could not find Financials Statements element with any selector")
                    browser.close()
                    return []
            
            # Create a temporary directory for downloads
            temp_dir = Path(__file__).resolve().parent.parent
            # with Path(__file__).resolve().parent.parent.parent as temp_dir:
            # Set up download behavior
            page.context.set_default_timeout(30000)
            
            # Function to download PDF from a link
            def download_pdf_from_link(link_element, index):
                try:
                    href = link_element.get_attribute("href")

                    if "FINANCIAL_STATEMENT" not in href and "FINANCIAL_STATEMENT" not in href:

                        return ""

                    if href and href.endswith('.pdf'):
                        # Get the filename from the href
                        filename = href.split('/')[-1]
                        if not filename.endswith('.pdf'):
                            filename += '.pdf'
                        
                        # Create full path for the download
                        download_path = os.path.join(temp_dir, "downloads",f"{index}_{filename}")
                        
                        # Download the PDF
                        with page.expect_download() as download_info:
                            link_element.click()
                        
                        download = download_info.value
                        download.save_as(download_path)
                        
                        print(f"Downloaded PDF: {download_path}")
                        downloaded_pdfs.append(download_path)
                        
                except Exception as e:
                    print(f"Error downloading PDF: {e}")
            
            # Process rows
            try:
                # random_loc = page.locator("table tbody tr")
                # print(f"Found {random_loc.count()} rows in the table")
                rows = page.locator(row_identifier)
                rows_count = rows.count()
                print(f"Found {rows_count} rows")
                
                for i in range(rows_count):
                    row = rows.nth(i)
                    # Look for anchor tag with PDF link in the row
                    pdf_links = row.locator("td a[href*='.pdf']")
                    link_count = pdf_links.count()
                    
                    for j in range(link_count):
                        link = pdf_links.nth(j)
                        download_pdf_from_link(link, f"{i}_{j}")
                        
            except Exception as e:
                print(f"Error processing even rows: {e}")
            
            # Alternative approach: look for all PDF links in the table
            if not downloaded_pdfs:
                print("Trying alternative approach to find PDF links")
                try:
                    all_pdf_links = page.locator("tbody#ngx_finStatement a[href*='.pdf']")
                    link_count = all_pdf_links.count()
                    print(f"Found {link_count} PDF links using alternative selector")
                    
                    for i in range(link_count):
                        link = all_pdf_links.nth(i)
                        download_pdf_from_link(link, f"alt_{i}")
                        
                except Exception as e:
                    print(f"Error with alternative approach: {e}")
            
            # Handle pagination - navigate through all pages
            print("Starting pagination handling...")
            page_number = 1
            
            while True:
                print(f"Processing page {page_number}")
                
                # Check if there's a next page button
                try:
                    # Find the current page button
                    current_page = page.locator("#latestdiclosuresDir_paginate span a.paginate_button.current")
                    if current_page.count() == 0:
                        print("No pagination found or already on first page")
                        break
                    
                    # Find all pagination buttons
                    pagination_buttons = page.locator("#latestdiclosuresDir_paginate span a")
                    button_count = pagination_buttons.count()
                    print("button count ",button_count,pagination_buttons)
                    
                    if button_count <= 1:
                        print("Only one page or no pagination buttons found")
                        break
                    
                    # Find the next page button (the one after current)
                    current_index = -1
                    for i in range(button_count):
                        button = pagination_buttons.nth(i)
                        print("button ", button)
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
                    
                    # Download PDFs from the new page using the same logic
                    page_pdfs_found = False
                    
                    # Process even rows on new page
                    try:
                        rows = page.locator(row_identifier)
                        rows_count = rows.count()
                        print(f"Found {rows_count} even rows on page {page_number + 1}")
                        
                        for i in range(rows_count):
                            row = rows.nth(i)
                            pdf_links = row.locator("td a[href*='.pdf']")
                            link_count = pdf_links.count()
                            
                            for j in range(link_count):
                                link = pdf_links.nth(j)
                                download_pdf_from_link(link, f"page{page_number + 1}_even_{i}_{j}")
                                page_pdfs_found = True
                                
                    except Exception as e:
                        print(f"Error processing even rows on page {page_number + 1}: {e}")
                    
                    # Alternative approach for new page if no PDFs found
                    if not page_pdfs_found:
                        print(f"Trying alternative approach on page {page_number + 1}")
                        try:
                            all_pdf_links = page.locator("#ngx_finStatement a[href*='.pdf']")
                            link_count = all_pdf_links.count()
                            print(f"Found {link_count} PDF links using alternative selector on page {page_number + 1}")
                            
                            for i in range(link_count):
                                link = all_pdf_links.nth(i)
                                download_pdf_from_link(link, f"page{page_number + 1}_alt_{i}")
                                
                        except Exception as e:
                            print(f"Error with alternative approach on page {page_number + 1}: {e}")
                    
                    page_number += 1
                    
                except Exception as e:
                    print(f"Error handling pagination on page {page_number}: {e}")
                    break
        
            browser.close()
            
    except Exception as e:
        print(f"Error in web automation: {e}")
        return []
    
    print(f"Successfully downloaded {len(downloaded_pdfs)} PDFs")
    
    return downloaded_pdfs


tries = 0

@tool
def get_financial_statements(ticker:str,stock_exchange:str="NGX") -> Dict[str, Any]:
    """
    Extract finanical statement information from NGX (Nigerian Stock Exchange) company profiles.
    
    This function performs comprehensive web automation to download and parse finanical statement PDFs
    from the NGX website, convert them to images
    
    Args:
        ticker (str): The stock ticker/symbol of the company (e.g., "ABCTRANS")
        stock_exchange (str): The stock exchange where the stock is listed. 
                             Currently only supports "NGX" (Nigerian Stock Exchange)
    
    Returns:
        list: A list of a list of dictionaries containing extracted finanical statement information.
              Each dictionary contains:all information extracted from the image gotten from the pdfs
              of finanical statements

    Example:
        get_financial_statements("ABCTRANS") -> [
            [
                {
                    "text_ocr": "This is a test",
                    "text_easyocr": "This is a test",
                    "text_advanced": "This is a test"
                }
            ]
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
    
    global financial_statements

    if len(financial_statements) > 0:

        return financial_statements

    url = f"https://ngxgroup.com/exchange/data/company-profile/?symbol={ticker}&directory=companydirectory"
    row_identifier = "div#financialstatement_wrapper table tbody tr"
    
    downloaded_pdfs = get_downloaded_pdfs(url, row_identifier)
    
    pdf_images = create_images_from_pdfs(downloaded_pdfs)
    text_content = read_images(pdf_images)
    
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

    if len(pdf_images) == 0 and tries < 2:
        print("No information extracted from PDFs.Will rerun once more")
        tries += 1
        return get_financial_statements(ticker, stock_exchange)
    
    
    financial_statements = text_content

    return text_content
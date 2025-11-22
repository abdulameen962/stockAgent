from pathlib import Path
from smolagents import tool
import os
from playwright.sync_api import sync_playwright
# import tempfile
import time
import camelot
import pandas as pd
import re

from tools.corporate_disclosures import create_images_from_pdfs
from tools.image_analysis import read_images

def normalize_spacing(text):
    """
    Normalize spacing in a string by reducing multiple consecutive spaces to single spaces.
    
    Args:
        text (str): The input string to normalize
        
    Returns:
        str: The string with normalized spacing (maximum one space between characters)
        
    Example:
        normalize_spacing("hello    world") -> "hello world"
        normalize_spacing("  multiple   spaces  ") -> "multiple spaces"
    """
    if not text or not isinstance(text, str):
        return text
    
    # Replace multiple consecutive spaces with a single space
    normalized = re.sub(r'\s+', ' ', text)
    
    # Remove leading and trailing spaces
    normalized = normalized.strip()
    
    return normalized

def read_one_pdf(path:str):

    tables = camelot.read_pdf(path, pages='all', flavor='lattice')

    pdf_info = []

    for table in tables:
        df = table.df
        # Print the DataFrame to see the extracted tables

        # convert pandas df to object
        df_object = df.to_dict(orient='records') # using different one would change the way you loop through them

        # for obj in df_object:

        #     for data in obj:

        #         val = obj[data]

        #         if not val:

        #             continue

        #         val_data = val.strip()

        #         # Split by line breaks and print index and value
        #         val_arr = val_data.splitlines() # because each str has \n for line breaks
                
        #         for idx, line in enumerate(val_arr):
        #             line = line.strip()

        #             if not line:

        #                 continue

        #             line = normalize_spacing(line)
        #             print(f"    [{idx}] {line}")
        #             # check for insider name
        #             if "director" in line.lower() or "insider" in line.lower():

        #                 insider_name = val_arr[idx + 1].strip() if idx + 1 < len(val_arr) else None
        #                 pdf_info['insider_name'] = insider_name

        #                 # print("found name",insider_name)

        #                 continue

        #             # check for position status
        #             if "position" in line.lower() or "status" in line.lower():

        #                 position_status = val_arr[idx - 1].strip() if idx < len(val_arr) else None
        #                 pdf_info['position_status'] = position_status

        #                 # print("found position status",position_status)

        #                 continue

        #             # check for name ticker
        #             if "name" in line.lower():
        #                 name_ticker = val_arr[idx + 1].strip() if idx + 1 < len(val_arr) else None
        #                 pdf_info['name_ticker'] = name_ticker

        #                 # print("found name ticker",name_ticker)

        #                 continue

        #             # check for description
        #             if "financial" in line.lower() or "description  of the financial" in line.lower():
        #                 description = val_arr[idx + 1].strip() if idx + 1 < len(val_arr) else None
        #                 pdf_info['description'] = description

        #                 # print("found description",description)

        #                 continue

        #             # check for nature of transaction
        #             if "nature of the transaction" in line.lower() or "nature" in line.lower():
        #                 nature_of_transaction = val_arr[idx - 1].strip() if idx < len(val_arr) else None
        #                 pdf_info['nature_of_transaction'] = nature_of_transaction

        #                 # print("found nature of transaction",nature_of_transaction)

        #                 continue

        #             # check for aggregate information
        #             if "aggregate information" in line.lower() or "information" in line.lower():
        #                 aggregate_total_price = val_arr[idx + 1].strip() if idx + 1 < len(val_arr) else None
        #                 aggregate_price = val_arr[idx + 4].strip() if idx + 4 < len(val_arr) else None
                        
        #                 aggregate_information = f"{aggregate_total_price} for averagely {aggregate_price} each"
        #                 pdf_info['aggregate_information'] = aggregate_information

        #                 # print("found aggregate information",aggregate_information)

        #                 continue

        #             # check for date of transaction
        #             if "date of transaction" in line.lower() or "date of" in line.lower():
        #                 date_of_transaction = val_arr[idx - 1].strip() if idx < len(val_arr) else None
        #                 pdf_info['date_of_transaction'] = date_of_transaction

        #                 # print("found date of transaction",date_of_transaction)

        #                 continue

        pdf_info.append(df_object)

    return pdf_info

def extract_information_from_pdfs(downloaded_pdfs):
    # Parse PDFs and extract information using camelot
    information_array = []
    
    for pdf_path in downloaded_pdfs:
        try:
            print(f"Processing PDF with camelot: {pdf_path}")
            
            pdf_info = []

            # Extract all tables from PDF using camelot
            tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')
            
            if not tables:
                tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')

                if not tables:
                    print(f"No tables found in {pdf_path}")
                    continue
            
            
            for table in tables:
                df = table.df
                # Print the DataFrame to see the extracted tables

                # convert pandas df to object
                df_object = df.to_dict(orient='records')

                pdf_info.append(df_object)

            if len(pdf_info) > 0:

                information_array.append(pdf_info)
            
        except Exception as e:
            print(f"Error processing PDF {pdf_path}: {e}")
            continue
    
    print(f"Successfully extracted information from {len(information_array)} PDFs")
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
            
            # Click on the "Director Dealings" span element
            try:
                # Look for the Director Dealings element within the specified structure
                director_dealings_selector = "li label span:has-text('Director Dealings')"
                page.wait_for_selector(director_dealings_selector, timeout=60000)
                page.click(director_dealings_selector)
                print("Successfully clicked on Director Dealings")
                time.sleep(3)  # Wait for the content to load after clicking
            except Exception as e:
                print(f"Could not find Director Dealings element: {e}")
                # Try alternative selectors
                alternative_selectors = [
                    "span:has-text('Director Dealings')",
                    "label:has-text('Director Dealings')",
                    "li:has-text('Director Dealings')"
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
                    print("Could not find Director Dealings element with any selector")
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
                    all_pdf_links = page.locator("tbody#ngx_dirDealings a[href*='.pdf']")
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
                            all_pdf_links = page.locator("#ngx_dirDealings a[href*='.pdf']")
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
def extract_director_disclosures(ticker:str,stock_exchange:str="NGX") -> list:
    """
    Extract director disclosure information from NGX (Nigerian Stock Exchange) company profiles.
    
    This function performs comprehensive web automation to download and parse director disclosure PDFs
    from the NGX website, convert them to images
    
    Args:
        ticker (str): The stock ticker/symbol of the company (e.g., "ABCTRANS")
        stock_exchange (str): The stock exchange where the stock is listed. 
                             Currently only supports "NGX" (Nigerian Stock Exchange)
    
    Returns:
        list: A list of a list of dictionaries containing extracted director disclosure information.
              Each dictionary contains:all information extracted from the image gotten from the pdfs
              of director disclosures

    Example:
        extract_director_disclosures("ABCTRANS") -> [
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

    url = f"https://ngxgroup.com/exchange/data/company-profile/?symbol={ticker}&directory=companydirectory"
    row_identifier = "div#latestdiclosuresDir_wrapper table tbody tr"
    
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
        return extract_director_disclosures(ticker, stock_exchange)

    return text_content
from smolagents import tool
import requests
import re
from typing import Optional, Dict, Any
import time
from playwright.sync_api import sync_playwright

@tool
def get_pe_ratio(ticker_symbol: str) -> Dict[str, Any]:
    """
    Extract P/E ratio of a company from the investing.com website
    
    This function scrapes the investing.com page to extract the current P/E ratio
    of a company(return 0 if error)
    
    Args:
        ticker_symbol (str): The ticker symbol of the company
        
    Returns:
        str - P/E ratio of the company
            
    Example:
        get_pe_ratio("ABCTRANS") -> "15.2x"
    """

    id_url = f"/pro/NGSE:{ticker_symbol}/explorer/pe_ltm"
    url = f"https://ng.investing.com/pro/NGSE:{ticker_symbol}/explorer/pe_ltm"
    
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
            time.sleep(3)  # Additional wait to ensure dynamic content loads

            print("Page loaded successfully.")

            pe_el = page.locator(f"a[href='{id_url}']")

            # print("P/E ratio element found:", pe_el)

            pe_ratio = pe_el.text_content()

            return pe_ratio

    except Exception as e:

        print("error ",e)

        return 0
        

    return pe_ratio

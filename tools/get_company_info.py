from smolagents import tool
from playwright.sync_api import sync_playwright
from typing import Dict
import time

@tool
def get_company_info(ticker: str) -> Dict:
    """
    Retrieves company information for a given ticker symbol.

    Args:
        ticker (str): The ticker symbol of the company.

    Returns:
        Dict: A dict containing information about the company.

    Example:
        get_company_info("ABCTRANS") ->  {
           "sector": "ICT",
           "Sub sector": "Telecommunication",
           "Market Cap (Mil.)": "62,500,000.00",
           "Shares Outstanding (Mil.)": "10,000,000.00",
           "Share price":"₦6.25",
        }
        
    
    Raises:
        ValueError: If stock_exchange is not "NGX" (currently only NGX is supported)
    """

    url = f"https://ngxgroup.com/exchange/data/company-profile/?symbol={ticker}&directory=companydirectory"
    stock_id = ".d-detailquote-head .d-dquote-bigContainer span.d-dquote-x3"
    sector_id = ".Sector"
    sub_sector_id = ".SubSector"
    market_cap_id = ".MarketCap"
    shares_outstanding_id = ".SharesOutstanding"

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

            stock_price_el = page.locator(f"{stock_id}")

            stock_price = stock_price_el.text_content()

            sector_el = page.locator(f"{sector_id}")
            sector = sector_el.text_content()

            sub_sector_el = page.locator(f"{sub_sector_id}")
            sub_sector = sub_sector_el.text_content()

            market_cap_el = page.locator(f"{market_cap_id}")
            market_cap = market_cap_el.text_content()

            shares_el = page.locator(f"{shares_outstanding_id}")
            shares = shares_el.text_content()

            return {
                "sector": sector,
                "Sub sector": sub_sector,
                "Market Cap (Mil.)": market_cap,
                "Shares Outstanding (Mil.)": shares,
                "Share price":stock_price,
            }

    except Exception as e:

        print("error ",e)

        return 0

    
    return f"Company information for {ticker}: This is a mock company with a 10% annual return." * 1000
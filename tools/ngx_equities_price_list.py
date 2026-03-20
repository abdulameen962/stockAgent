"""
Scrape NGX equities price list table across paginated pages.

Source: https://ngxgroup.com/exchange/data/equities-price-list/
"""

from __future__ import annotations

import re
import time
from typing import List

from playwright.sync_api import Page, sync_playwright
from smolagents import tool

NGX_EQUITIES_URL = "https://ngxgroup.com/exchange/data/equities-price-list/"
TBODY_SELECTOR = "tbody#ngx_equities_trading_statistics"
PAGINATE_BUTTON = ".dataTables_paginate .paginate_button"
MAX_PAGE = 6


def _strip_bracket_suffixes(text: str) -> str:
    """e.g. 'FTNCOCOA [RST]' -> 'FTNCOCOA'. Removes every ` [ ... ]` segment."""
    cleaned = re.sub(r"\s*\[[^\]]*\]", "", text)
    return re.sub(r"\s+", " ", cleaned).strip()


def _dismiss_cookies_if_present(page: Page) -> None:
    for sel in (
        "button:has-text('ACCEPT')",
        "a.cmplz-accept",
        "#cmplz-btn-accept",
        "button:has-text('Accept')",
    ):
        try:
            loc = page.locator(sel).first
            if loc.is_visible(timeout=2000):
                loc.click()
                time.sleep(0.5)
                return
        except Exception:
            continue


def _collect_tbody_anchor_texts(page: Page) -> List[str]:
    tbody = page.locator(TBODY_SELECTOR)
    tbody.wait_for(state="visible", timeout=90_000)
    links = tbody.locator("a")
    n = links.count()
    out: List[str] = []
    for i in range(n):
        raw = links.nth(i).text_content()
        if raw:
            s = raw.strip()
            if s:
                out.append(s)
    return out


def _click_paginate_page(page: Page, page_num: int) -> bool:
    """Clicks numbered page control (exact match, avoids e.g. '12' for '2'). Returns False if missing/disabled."""
    btn = page.locator(PAGINATE_BUTTON).filter(has_text=re.compile(rf"^\s*{page_num}\s*$"))
    if btn.count() == 0:
        return False
    first = btn.first
    cls = first.get_attribute("class") or ""
    if "disabled" in cls:
        return False
    first.click()
    time.sleep(1.5)
    try:
        page.wait_for_load_state("networkidle", timeout=30_000)
    except Exception:
        pass
    return True


def fetch_ngx_equities_price_list_cleaned() -> List[str]:
    """
    Opens the NGX equities price list, walks pages 1–6, collects every `<a>` text
    under `tbody#ngx_equities_trading_statistics`, then strips bracket tags like `[MRF]`.

    Returns:
        Cleaned strings in scrape order (whitespace normalized, bracket segments removed).

    Example:
        ``FTNCOCOA [RST]`` -> ``FTNCOCOA``
    """
    collected: List[str] = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                context = browser.new_context()
                page = context.new_page()
                page.goto(NGX_EQUITIES_URL, wait_until="networkidle", timeout=120_000)
                _dismiss_cookies_if_present(page)
                page.wait_for_selector(TBODY_SELECTOR, timeout=90_000)

                for page_idx in range(1, MAX_PAGE + 1):
                    if page_idx > 1:
                        if not _click_paginate_page(page, page_idx):
                            print(
                                f"ngx_equities_price_list: stop pagination at page {page_idx} "
                                "(control missing or disabled)"
                            )
                            break
                    collected.extend(_collect_tbody_anchor_texts(page))
            finally:
                browser.close()
    except Exception as e:
        print("ngx_equities_price_list error:", e)
        return []

    return [c for raw in collected if (c := _strip_bracket_suffixes(raw))]


@tool
def get_ngx_equities_price_list_symbols() -> List[str]:
    """
    Scrape NGX listed symbols from the delayed equities price table (pages 1–6).

    Collects all ``<a>`` text under ``tbody#ngx_equities_trading_statistics``, then
    removes bracket suffixes (e.g. ``ACCESSCORP [MRF]`` -> ``ACCESSCORP``).
    """
    return fetch_ngx_equities_price_list_cleaned()

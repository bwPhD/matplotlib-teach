#!/usr/bin/env python3
"""Wake a Streamlit Community Cloud app from GitHub Actions.

The script uses a real browser because Streamlit's sleep page sometimes
requires clicking the wake-up button. A plain HTTP request can report success
while still leaving the app asleep.
"""

from __future__ import annotations

import os
import re
import sys
import time
from datetime import datetime, timezone

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, sync_playwright


DEFAULT_URL = "https://www.aimust.online/"
WAKE_BUTTON_RE = re.compile(r"get this app back up|wake.*app|yes", re.IGNORECASE)
SLEEP_TEXT_RE = re.compile(r"gone to sleep|Zzzz|inactivity", re.IGNORECASE)


def log(message: str) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{timestamp}] {message}", flush=True)


def get_target_url() -> str:
    url = os.getenv("STREAMLIT_URL", DEFAULT_URL).strip()
    if not url:
        return DEFAULT_URL
    if not url.startswith(("http://", "https://")):
        raise ValueError("STREAMLIT_URL must start with http:// or https://")
    return url


def click_wake_button_if_present(page: Page) -> bool:
    sleep_text = page.get_by_text(SLEEP_TEXT_RE, exact=False)
    sleep_visible = False

    try:
        sleep_text.first.wait_for(state="visible", timeout=5_000)
        sleep_visible = True
    except PlaywrightTimeoutError:
        sleep_visible = False

    if not sleep_visible:
        log("No Streamlit sleep page detected.")
        return False

    log("Streamlit sleep page detected. Looking for the wake button.")
    button = page.get_by_role("button", name=WAKE_BUTTON_RE)

    try:
        button.first.click(timeout=15_000)
        log("Wake button clicked.")
        return True
    except PlaywrightTimeoutError:
        log("Wake button was not found before timeout.")
        return False


def wait_for_app(page: Page) -> None:
    """Give Streamlit enough time to boot and establish a frontend session."""
    try:
        page.wait_for_load_state("networkidle", timeout=60_000)
    except PlaywrightTimeoutError:
        log("Network did not become idle; continuing because Streamlit may keep connections open.")

    for selector in [
        "[data-testid='stAppViewContainer']",
        "[data-testid='stHeader']",
        "section.main",
        ".stApp",
    ]:
        try:
            page.locator(selector).first.wait_for(timeout=30_000)
            log(f"Detected Streamlit app element: {selector}")
            break
        except PlaywrightTimeoutError:
            continue

    page.mouse.wheel(0, 500)
    time.sleep(2)
    page.mouse.wheel(0, -500)
    time.sleep(8)


def main() -> int:
    url = get_target_url()
    log(f"Target URL: {url}")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1366, "height": 900},
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120 Safari/537.36"
            ),
        )
        page = context.new_page()

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=90_000)
            clicked = click_wake_button_if_present(page)
            if clicked:
                wait_for_app(page)
            else:
                wait_for_app(page)

            log(f"Final page title: {page.title()!r}")
            log("Wake check completed.")
            return 0
        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        log(f"Wake check failed: {exc}")
        raise SystemExit(1)

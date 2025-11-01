import pytest

pytestmark = pytest.mark.e2e

def _wait_for_value_change(page):
    # Wait until the #value text is no longer the initial em-dash
    page.wait_for_function("document.querySelector('#value').textContent.trim() !== '—'", timeout=5000)

def test_user_can_calculate_sum(playwright, live_server):
    browser = playwright.chromium.launch()
    page = browser.new_page()
    try:
        page.goto(live_server, wait_until="domcontentloaded")
        page.fill("#a", "10")
        page.select_option("#op", "add")
        page.fill("#b", "7")
        page.click("#calc")
        _wait_for_value_change(page)
        assert page.text_content("#value").strip() in {"17", "17.0"}
    finally:
        browser.close()

def test_user_divide_by_zero_error(playwright, live_server):
    browser = playwright.chromium.launch()
    page = browser.new_page()
    try:
        page.goto(live_server, wait_until="domcontentloaded")
        page.fill("#a", "1")
        page.select_option("#op", "divide")
        page.fill("#b", "0")
        page.click("#calc")
        _wait_for_value_change(page)
        text = page.text_content("#value").strip()
        assert "error" in text.lower()
    finally:
        browser.close()

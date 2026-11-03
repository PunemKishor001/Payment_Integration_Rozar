import re
from datetime import datetime
from pathlib import Path

import allure
import pytest
from allure_commons.types import AttachmentType
from playwright.sync_api import sync_playwright, Page

from utilities.logger import get_logger, LOG_FILE

logger = get_logger("Conftest")

# Attach only the current test's logs to Allure
@pytest.fixture(autouse=True)
def attach_test_logs_to_allure():
    start_position = LOG_FILE.stat().st_size if LOG_FILE.exists() else 0

    yield

    if LOG_FILE.exists():
        log_data = LOG_FILE.read_bytes()[start_position:]
        test_logs = log_data.decode("utf-8", errors="replace")

        if test_logs:
            allure.attach(
                test_logs,
                name="Execution Logs",
                attachment_type=AttachmentType.TEXT
            )


@pytest.fixture
def launch_browser():
    logger.info("Launching Chromium browser")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("http://localhost:5500/?utm_source=chatgpt.com")
        print("Print Url: ",page.url)
        logger.info(f"Browser opened successfully: {page.url}")

        yield page

        logger.info("Closing browser")

        browser.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item,call):
    outcome = yield
    report = outcome.get_result()
    # Capture screenshot only when test execution fails
    if report.when == "call" and report.failed:
        logger.error(f"Test failed: {item.nodeid}")
        # Find Playwright Page fixture
        page = next(
                (
                    fixture
                    for fixture in item.funcargs.values()
                    if isinstance(fixture, Page)
                ),
                None
            )

        if page is None:
             logger.error("Page not available for failure screenshot")
             return

        screenshot_dir = (
                    Path(__file__).resolve().parent / "screenshots"
            )

        screenshot_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        test_name = re.sub(
                r"[^A-Za-z0-9_-]",
                "_",
                item.name
            )

        screenshot_path = (
                    screenshot_dir /
                    f"FAILED_{test_name}_{timestamp}.png"
            )

        try:
            page.screenshot(
                    path=str(screenshot_path),
                    full_page=True
                )

            logger.error(
                    f"Failure screenshot saved: {screenshot_path}"
                )

        except Exception:
            logger.exception("Screenshot capture failed")

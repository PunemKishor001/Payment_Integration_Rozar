import json
from pathlib import Path

import pytest
from playwright.sync_api import Page
from conftest import launch_browser
from pages.login import LoginPage

# Read JSON test data
data_file = (
    Path(__file__).resolve().parent.parent
    / "test_data"
    / "login_data.json"
)

with open(data_file, "r", encoding="utf-8") as file:
    login_data = json.load(file)

@pytest.fixture
def logged_in_page(launch_browser: Page):
    page = launch_browser
    test_data = login_data[0]
    loginPages = LoginPage(page)
    loginPages.username_input(test_data["username"])
    loginPages.password_input(test_data["password"])
    loginPages.login_button()
    page.wait_for_url("**/inventory.html")

    return page

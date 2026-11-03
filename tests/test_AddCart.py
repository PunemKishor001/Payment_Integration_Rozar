import json
from pathlib import Path

import allure
import pytest
from sympy.abc import lamda

from tests.test_login import logged_in_page
from playwright.sync_api import Page, expect
from pages.addcart import AddCart

data_file = (
    Path(__file__).resolve().parent.parent
    / "test_data"
    / "checkout_data.json"
)

with open(data_file, "r", encoding="utf-8") as file:
    checkout_data = json.load(file)

@pytest.mark.parametrize("test_data", checkout_data,ids=lambda data: data["test_name"])
@allure.epic("E-commerce Application")
@allure.feature("Shopping Cart and Checkout")
@allure.story("Add backpack and complete checkout")
@allure.title("Verify backpack purchase flow")
@allure.severity(allure.severity_level.CRITICAL)
def test_addcart(logged_in_page: Page,test_data):
    page = logged_in_page
    cart = AddCart(page,test_data)
    # Add product to cart
    with allure.step("Add backpack to cart"):
        cart.add_backpack_to_cart()

    # Open cart
    with allure.step("Open shopping cart"):
        cart.open_cart()

    # Checkout
    with allure.step("Proceed to checkout"):
        cart.proceed_to_checkout()
        cart.enter_checkout_details()

    # Razorpay payment
    with allure.step("Complete Razorpay sandbox payment"):
        cart.click_payment()
        cart.enter_razorpay_card_details()
        cart.skip_save_card()
        # Complete demo payment
        cart.complete_demo_payment()

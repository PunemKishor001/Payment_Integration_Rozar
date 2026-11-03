import json
from pathlib import Path

import allure
import pytest
from sympy.abc import lamda

from tests.test_login import logged_in_page
from playwright.sync_api import Page, expect
from pages.Negativepayment import NegativePayment

data_file = (
    Path(__file__).resolve().parent.parent
    / "test_data"
    / "negative_payment_data.json"
)

with open(data_file, "r", encoding="utf-8") as file:
    checkout_data = json.load(file)

# NEG_001 - Invalid Card Number
@pytest.mark.parametrize("test_data",
[data for data in checkout_data if data["scenario"] == "invalid_card"],
    ids=lambda data: data["test_name"])
@allure.epic("E-commerce Application")
@allure.feature("Payment Gateway Testing")
@allure.story("Negative Payment Testing")
@allure.severity(allure.severity_level.CRITICAL)
def test_invalidcardnumer(logged_in_page: Page,test_data):
    allure.dynamic.title(
        f"{test_data['test_id']} - {test_data['test_name']}"
    )

    allure.dynamic.description(
        "Verify payment gateway validation for an invalid card number."
    )
    page = logged_in_page
    cart = NegativePayment(page, test_data)
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
        cart.enter_razorpay_invalidcard_details()

# NEG_002 - Expired Card
@pytest.mark.parametrize("test_data",
[data for data in checkout_data if data["scenario"] == "expired_card"],
    ids=lambda data: data["test_name"])
@allure.epic("E-commerce Application")
@allure.feature("Payment Gateway Testing")
@allure.story("Negative Payment Testing")
@allure.severity(allure.severity_level.CRITICAL)
def test_expiredcard(logged_in_page: Page,test_data):
    allure.dynamic.title(
        f"{test_data['test_id']} - {test_data['test_name']}"
    )

    allure.dynamic.description(
        "Verify payment gateway validation for an invalid card number."
    )
    page = logged_in_page
    cart = NegativePayment(page, test_data)
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
        cart.enter_razorpay_carddetails_Expiredcard()

# NEG_003 - Invalid Cvv
@pytest.mark.parametrize("test_data",
[data for data in checkout_data if data["scenario"] == "Invlaid_CVv"],
    ids=lambda data: data["test_name"])
@allure.epic("E-commerce Application")
@allure.feature("Payment Gateway Testing")
@allure.story("Negative Payment Testing")
@allure.severity(allure.severity_level.CRITICAL)
def test_invalidcvv(logged_in_page: Page,test_data):
    allure.dynamic.title(
        f"{test_data['test_id']} - {test_data['test_name']}"
    )

    allure.dynamic.description(
        "Verify payment gateway validation for an invalid card number."
    )
    page = logged_in_page
    cart = NegativePayment(page, test_data)
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
        cart.enter_razorpay_carddetails_InvalidCvv()

# NEG_004 - Invalid Otp
@pytest.mark.parametrize("test_data",
[data for data in checkout_data if data["scenario"] == "Invlaid_otp"],
    ids=lambda data: data["test_name"])
@allure.epic("E-commerce Application")
@allure.feature("Payment Gateway Testing")
@allure.story("Negative Payment Testing")
@allure.severity(allure.severity_level.CRITICAL)
def test_invaildotp(logged_in_page: Page,test_data):
    allure.dynamic.title(
        f"{test_data['test_id']} - {test_data['test_name']}"
    )

    allure.dynamic.description(
        "Verify payment gateway validation for an invalid card number."
    )
    page = logged_in_page
    cart = NegativePayment(page, test_data)
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
        cart.invalid_otp()

# NEG_005 - empty_otp
@pytest.mark.parametrize("test_data",
[data for data in checkout_data if data["scenario"] == "Empty_otp"],
    ids=lambda data: data["test_name"])
@allure.epic("E-commerce Application")
@allure.feature("Payment Gateway Testing")
@allure.story("Negative Payment Testing")
@allure.severity(allure.severity_level.CRITICAL)
def test_emptyotp(logged_in_page: Page,test_data):
    allure.dynamic.title(
        f"{test_data['test_id']} - {test_data['test_name']}"
    )

    allure.dynamic.description(
        "Verify payment gateway validation for an invalid card number."
    )
    page = logged_in_page
    cart = NegativePayment(page, test_data)
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
        cart.empty_otp()


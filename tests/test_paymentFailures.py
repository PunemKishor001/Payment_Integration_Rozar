import json
from pathlib import Path

import allure
import pytest
from sympy.abc import lamda

from tests.test_login import logged_in_page
from playwright.sync_api import Page, expect
from pages.PaymentFailure import paymentfailue

data_file = (
    Path(__file__).resolve().parent.parent
    / "test_data"
    / "paymentfailure_data.json"
)

with open(data_file, "r", encoding="utf-8") as file:
    checkout_data = json.load(file)

@pytest.mark.parametrize("test_data",
                         [data for data in checkout_data if data["scenario"] == "Valid_DebitCard"],
                         ids=lambda data: data["test_name"]
                         )
@allure.epic("E-commerce Application")
@allure.feature("Shopping Cart and Checkout")
@allure.story("Add backpack and complete checkout")
@allure.title("Verify backpack purchase flow")
@allure.severity(allure.severity_level.CRITICAL)
def test_payment_failure(logged_in_page: Page,test_data):
    page = logged_in_page
    cart = paymentfailue(page,test_data)
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
        cart.payment_failed()

@pytest.mark.parametrize("test_data",
                         [data for data in checkout_data if data["scenario"] == "Valid_DebitCard"],
                         ids=lambda data: data["test_name"]
                         )
@allure.epic("E-commerce Application")
@allure.feature("Shopping Cart and Checkout")
@allure.story("Add backpack and retry payment flow with complete checkout")
@allure.title("Verify retry purchase flow")
@allure.severity(allure.severity_level.CRITICAL)
def test_retrypayment_failure(logged_in_page: Page,test_data):
    page = logged_in_page
    cart = paymentfailue(page,test_data)
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
        cart.retry_payment_failed()
        #retryin the paymnet with same details
        cart.skip_save_card()
        cart.complete_demo_payment()

@pytest.mark.parametrize("test_data",
                         [data for data in checkout_data if data["scenario"] == "Valid_DebitCard"],
                         ids=lambda data: data["test_name"]
                         )
@allure.epic("E-commerce Application")
@allure.feature("Shopping Cart and Checkout")
@allure.story("Add backpack and enter card details come back to checkout page")
@allure.title("Verify after entering the card details closing the pop_up and comeback to the overview flow")
@allure.severity(allure.severity_level.CRITICAL)
def test_paymentcancellations(logged_in_page: Page,test_data):
    page = logged_in_page
    cart = paymentfailue(page,test_data)
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
        cart.enter_razorpaycard_details()
        cart.Paymentcancellation()

@pytest.mark.parametrize("test_data",
                         [data for data in checkout_data if data["scenario"] == "Valid_CreditCard"],
                         ids=lambda data: data["test_name"]
                         )
@allure.epic("E-commerce Application")
@allure.feature("Shopping Cart and Checkout")
@allure.story("Add backpack and enter card details come back to checkout page")
@allure.title("Verify after entering the card details user not entering the otp")
@allure.severity(allure.severity_level.CRITICAL)
def test_Payment_sessiontimeout(logged_in_page: Page,test_data):
    page = logged_in_page
    cart = paymentfailue(page,test_data)
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
        cart.enter_razorpaycard_details()
        cart.skip_save_card()
        cart.payment_sessiontimeout()

@pytest.mark.parametrize("test_data",
                         [data for data in checkout_data if data["scenario"] == "Valid_CreditCard"],
                         ids=lambda data: data["test_name"]
                         )
@allure.epic("E-commerce Application")
@allure.feature("Shopping Cart and Checkout")
@allure.story("Add backpack and enter card details come back to checkout page")
@allure.title("Verify after entering the card details user not entering the otp")
@allure.severity(allure.severity_level.CRITICAL)
def test_retryPayment_aftersessiontimeout(logged_in_page: Page,test_data):
    page = logged_in_page
    cart = paymentfailue(page,test_data)
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
        cart.enter_razorpaycard_details()
        cart.skip_save_card()
        cart.payment_sessiontimeout()
        # Complete demo payment
        cart.click_cardslable_failed()
        # retryin the paymnet with same details
        cart.skip_save_card()
        cart.complete_demo_payment()
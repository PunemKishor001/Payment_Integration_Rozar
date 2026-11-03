from datetime import datetime
import json
from pathlib import Path

import allure
from allure_commons.types import AttachmentType

from utilities.logger import get_logger
from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError

# Read JSON test data
data_file = (
    Path(__file__).resolve().parent.parent
    / "test_data"
    / "negative_payment_data.json"
)

with open(data_file, "r", encoding="utf-8") as file:
    checkout_data = json.load(file)

class NegativePayment:
    def __init__(self, page: Page,data:dict):
        self.page = page
        self.data = data

        self.logger = get_logger(self.__class__.__name__)
        self.logger.info("Initializing AddCart page")
        # Inventory page
        self.backpack = page.locator(".inventory_item").filter(
            has_text="Sauce Labs Backpack"
        )
        self.add_to_cart_button = self.backpack.get_by_role(
            "button", name="ADD TO CART"
        )
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        # Cart page
        self.cart_title = page.get_by_text("Your Cart", exact=True)
        self.backpack_name = page.get_by_text(
            "Sauce Labs Backpack", exact=True
        )
        self.checkout_link = page.get_by_role(
            "link", name="CHECKOUT"
        )

        # Checkout information
        self.first_name = page.get_by_role(
            "textbox", name="First Name"
        )
        self.last_name = page.get_by_role(
            "textbox", name="Last Name"
        )
        self.zip_code = page.get_by_role(
            "textbox", name="Zip/Postal Code"
        )
        self.continue_button = page.get_by_role(
            "button", name="CONTINUE"
        )

        # Checkout overview and payment
        self.overview_title = page.get_by_text(
            "Checkout: Overview", exact=True
        )
        self.payment_button = page.get_by_role(
            "button", name="PAY WITH RAZORPAY"
        )

        self.logger.info("AddCart page initialized successfully")

    def add_backpack_to_cart(self):
        self.logger.info("Adding Sauce Labs Backpack to cart")
        self.add_to_cart_button.click()
        expect(self.cart_badge).to_have_text("1")
        self.logger.info("Backpack added to cart successfully")

    def open_cart(self):
        self.logger.info("Opening shopping cart")
        self.cart_link.click()
        expect(self.cart_title).to_be_visible()
        expect(self.backpack_name).to_be_visible()
        self.logger.info("Cart page opened and backpack verified")

    def proceed_to_checkout(self):
        self.logger.info("Proceeding to checkout")
        self.checkout_link.click()
        self.logger.info("Checkout page opened")

    def enter_checkout_details(self):
        self.logger.info("Entering checkout information")
        self.first_name.fill(self.data["firstname"])
        self.last_name.fill(self.data["lastname"])
        self.zip_code.fill(self.data["zip_code"])
        self.logger.info("Checkout information entered")
        self.continue_button.click()

        expect(self.overview_title).to_be_visible()
        self.logger.info("Checkout overview verified successfully")

    def click_payment(self):
        self.logger.info("Clicking Razorpay payment button")
        self.payment_button.click()
        self.logger.info("Razorpay payment initiated")

    def enter_razorpay_card_details(self):
        self.logger.info("Entering Razorpay payment details")
        razorpay = self.page.frame_locator("iframe")

        self.mobile = razorpay.get_by_test_id("contactNumber")
        self.card_number = razorpay.get_by_role(
            "textbox", name="Card Number"
        )
        self.expiry = razorpay.get_by_role(
            "textbox", name="MM / YY"
        )
        self.cvv = razorpay.get_by_role(
            "textbox", name="CVV"
        )

        expect(self.mobile).to_be_visible()
        self.mobile.fill(str(self.data["mobilenumber"]))

        expect(self.card_number).to_be_visible()
        expect(self.expiry).to_be_visible()
        expect(self.cvv).to_be_visible()

        # Use only the payment provider's documented test credentials.
        self.card_number.fill(str(self.data["cardnumber"]))
        self.expiry.fill(str(self.data["ExpiryDate"]))
        self.cvv.fill(str(self.data["cvvnumber"]))
        self.logger.info("Payment form details entered")
        self.page.wait_for_timeout(5000)
        continue_button = razorpay.get_by_role(
            "button", name="Continue", exact=True
        )

        expect(continue_button).to_be_enabled(timeout=15000)
        continue_button.click()

    def enter_razorpay_invalidcard_details(self):
        self.logger.info("Entering Razorpay payment details")
        razorpay = self.page.frame_locator("iframe")

        self.mobile = razorpay.get_by_test_id("contactNumber")
        self.card_number = razorpay.get_by_role(
            "textbox", name="Card Number"
        )
        self.expiry = razorpay.get_by_role(
            "textbox", name="MM / YY"
        )
        self.cvv = razorpay.get_by_role(
            "textbox", name="CVV"
        )

        expect(self.mobile).to_be_visible()
        self.mobile.fill(str(self.data["mobilenumber"]))

        expect(self.card_number).to_be_visible()
        expect(self.expiry).to_be_visible()
        expect(self.cvv).to_be_visible()

        # Use only the payment provider's documented test credentials.
        self.card_number.fill(str(self.data["cardnumber"]))
        self.expiry.fill(str(self.data["ExpiryDate"]))
        self.cvv.fill(str(self.data["cvvnumber"]))
        self.logger.info("Payment form details entered")
        self.page.wait_for_timeout(5000)
        continue_button = razorpay.get_by_role(
            "button", name="Continue", exact=True
        )

        expect(continue_button).to_be_enabled(timeout=15000)
        continue_button.click()
        self.logger.info("Verifying invalid card number validation")
        invalidcard_lable = razorpay.get_by_text(" Please enter a valid card number",exact=True)
        expect(invalidcard_lable).to_be_visible(timeout=10000)
        self.logger.info("Invalid card number validation displayed successfully")

    def enter_razorpay_carddetails_Expiredcard(self):
        self.logger.info("Entering Razorpay payment details")
        razorpay = self.page.frame_locator("iframe")

        self.mobile = razorpay.get_by_test_id("contactNumber")
        self.card_number = razorpay.get_by_role(
            "textbox", name="Card Number"
        )
        self.expiry = razorpay.get_by_role(
            "textbox", name="MM / YY"
        )
        self.cvv = razorpay.get_by_role(
            "textbox", name="CVV"
        )

        expect(self.mobile).to_be_visible()
        self.mobile.fill(str(self.data["mobilenumber"]))

        expect(self.card_number).to_be_visible()
        expect(self.expiry).to_be_visible()
        expect(self.cvv).to_be_visible()

        # Use only the payment provider's documented test credentials.
        self.card_number.fill(str(self.data["cardnumber"]))
        self.expiry.fill(str(self.data["ExpiryDate"]))
        self.cvv.fill(str(self.data["cvvnumber"]))
        self.logger.info("Payment form details entered")
        self.page.wait_for_timeout(5000)
        continue_button = razorpay.get_by_role(
            "button", name="Continue", exact=True
        )

        expect(continue_button).to_be_enabled(timeout=15000)
        continue_button.click()
        self.logger.info("Verifying card expiry date validation")
        invalidcard_lable = razorpay.get_by_text(" Please enter a valid expiry date",exact=True)
        expect(invalidcard_lable).to_be_visible(timeout=10000)
        self.logger.info("Card Expiry date validation displayed successfully")

    def enter_razorpay_carddetails_InvalidCvv(self):
        self.logger.info("Entering Razorpay payment details")
        razorpay = self.page.frame_locator("iframe")

        self.mobile = razorpay.get_by_test_id("contactNumber")
        self.card_number = razorpay.get_by_role(
            "textbox", name="Card Number"
        )
        self.expiry = razorpay.get_by_role(
            "textbox", name="MM / YY"
        )
        self.cvv = razorpay.get_by_role(
            "textbox", name="CVV"
        )

        expect(self.mobile).to_be_visible()
        self.mobile.fill(str(self.data["mobilenumber"]))

        expect(self.card_number).to_be_visible()
        expect(self.expiry).to_be_visible()
        expect(self.cvv).to_be_visible()

        # Use only the payment provider's documented test credentials.
        self.card_number.fill(str(self.data["cardnumber"]))
        self.expiry.fill(str(self.data["ExpiryDate"]))
        self.cvv.fill(str(self.data["cvvnumber"]))
        self.logger.info("Payment form details entered")
        self.page.wait_for_timeout(5000)
        continue_button = razorpay.get_by_role(
            "button", name="Continue", exact=True
        )

        expect(continue_button).to_be_enabled(timeout=15000)
        continue_button.click()
        self.logger.info("Verifying Invalid cvv number validation")
        invalidcard_lable = razorpay.get_by_text(" Please enter a 3 digit cvv",exact=True)
        expect(invalidcard_lable).to_be_visible(timeout=10000)
        self.logger.info("Invalid cvv number validation displayed successfully")

    def select_payment_failure(self):

        self.logger.info("Selecting payment failure")

        if not self.payment_page:
            raise RuntimeError("Payment page is not available")

        failure_button = self.payment_page.get_by_role(
            "button", name="Failure"
        )

        expect(failure_button).to_be_visible()
        failure_button.click()

        self.logger.info("Payment failure selected")

    def skip_save_card(self):
        self.logger.info("Skipping save card option")

        razorpay = self.page.frame_locator("iframe")

        save_cards = razorpay.get_by_role(
            "button", name="Maybe later"
        )

        expect(save_cards).to_be_visible(timeout=15000)

        try:
            with self.page.context.expect_page(timeout=5000) as new_page:
                save_cards.click()

            self.payment_page = new_page.value
            self.payment_page.wait_for_load_state()

            self.logger.info("New payment tab opened successfully")

        except PlaywrightTimeoutError:
            self.payment_page = None
            self.logger.info("No new tab opened")

    def debug_payment_frames(self):
        self.logger.info("Inspecting payment frames")

        for index, frame in enumerate(self.page.frames):
            print(f"\n--- FRAME {index} ---")
            print("URL:", frame.url)

            print(
                "OTP count:",
                frame.locator('input[name="otp"]').count()
            )

            print(
                "Buttons:",
                frame.get_by_role("button").all_text_contents()
            )

    def complete_demo_payment(self):

        if self.payment_page:
            success_button = self.payment_page.get_by_role(
                "button", name="Success"
            )

            failure_button = self.payment_page.get_by_role(
                "button", name="Failure"
            )

            expect(success_button).to_be_visible(timeout=10000)
            expect(failure_button).to_be_visible(timeout=10000)

            success_button.click()

            self.logger.info("Payment Success selected")

        else:
            # Handle OTP flow for test_data[1]
            razorpay = self.page.frame_locator("iframe")
            otp = razorpay.locator('input[name="otp"]')

            expect(otp).to_be_visible(timeout=15000)
            otp.fill(str(self.data["otp"]))

            otp_continue = razorpay.locator(
                'button[type="submit"][name="button"]'
            )

            expect(otp_continue).to_be_visible(timeout=15000)
            expect(otp_continue).to_be_enabled()

            otp_continue.click()

            self.logger.info("OTP submitted successfully")
        success_message = self.page.get_by_text(
            "THANK YOU FOR YOUR ORDER",
            exact=True
        )

        expect(success_message).to_be_visible(timeout=15000)
        self.logger.info("Order confirmation message displayed successfully")

    def invalid_otp(self):

        self.logger.info("Testing incorrect OTP")

        # OTP flow inside Razorpay iframe
        razorpay = self.page.frame_locator("iframe")

        otp = razorpay.locator('input[name="otp"]')

        expect(otp).to_be_visible(timeout=15000)

        # Enter incorrect OTP
        otp.fill(str(self.data["otp"]))

        otp_continue = razorpay.locator(
                'button[type="submit"][name="button"]'
            )

        expect(otp_continue).to_be_visible(timeout=15000)
        expect(otp_continue).to_be_enabled()

        otp_continue.click()

        self.logger.info("Incorrect OTP submitted")

        # Verify payment gateway error
        otp_error = razorpay.get_by_text(
                "Payment could not be completed",
                exact=True
            )

        expect(otp_error).to_be_visible(timeout=10000)

        self.logger.info("Incorrect OTP validation verified")

    def empty_otp(self):
        self.logger.info("Testing empty OTP validation")

        # OTP flow inside Razorpay iframe
        razorpay = self.page.frame_locator("iframe")

        otp = razorpay.locator('input[name="otp"]')

        expect(otp).to_be_visible(timeout=15000)

        # Enter incorrect OTP
        otp.clear()

        otp_continue = razorpay.locator(
                'button[type="submit"][name="button"]'
            )

        expect(otp_continue).to_be_visible(timeout=15000)
        expect(otp_continue).to_be_enabled()

        otp_continue.click()

        self.logger.info("Clicked Continue with empty OTP")

        # Verify OTP field remains empty
        expect(otp).to_have_value("")

        self.logger.info("Empty OTP validation verified successfully")

        screenshot_dir = (
                Path(__file__).resolve().parent.parent / "screenshots"
        )
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        screenshot_path = (
                screenshot_dir / f"payment_success_{timestamp}.png"
        )

        screenshot = self.page.screenshot(
            path=str(screenshot_path),
            full_page=True
        )

        self.logger.info(f"Payment screenshot saved: {screenshot_path}")

        allure.attach(
            screenshot,
            name=f"{self.data['test_name']}_Payment_Screenshot",
            attachment_type=AttachmentType.PNG
        )

        self.logger.info("Payment screenshot attached to Allure")

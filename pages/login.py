from playwright.sync_api import Page

from utilities.logger import get_logger


class LoginPage:
    def __init__(self,page:Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)
        self.username = page.get_by_role("textbox", name="Username")
        self.password = page.get_by_role("textbox", name="Password")
        self.login_btn = page.get_by_role("button", name="LOGIN")

    def username_input(self, username: str):
        self.logger.info("Entering username")
        self.username.fill(username)

    def password_input(self, password: str):
        self.logger.info("Entering password")
        self.password.fill(password)

    def login_button(self):
        self.logger.info("Clicking login button")
        self.login_btn.click()
        self.logger.info("Login button clicked successfully")
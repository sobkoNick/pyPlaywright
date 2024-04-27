from playwright.sync_api import Page
from reportportal_client import step


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = '#content-desktop #user_email'
        self.password_input = '#content-desktop #user_password'
        self.sing_in_btn = '#content-desktop [type="submit"]'

    @step
    def login(self, login_url, credentials):
        self.open_login_page(login_url)
        self.fill_email(credentials.username)
        self.fill_password(credentials.password)
        self.press_sign_in()
        return self

    @step
    def open_login_page(self, login_url):
        self.page.goto(login_url)
        return self

    @step
    def fill_email(self, email):
        self.page.locator(self.email_input).type(email)
        return self

    @step
    def fill_password(self, password):
        self.page.locator(self.password_input).type(password)
        return self

    @step
    def press_sign_in(self):
        self.page.locator(self.sing_in_btn).click()
        return self

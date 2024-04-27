from playwright.sync_api import Page, expect
from reportportal_client import step


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.signed_in_alert = '[class="common-flash-info"]'
        self.user_menu_btn = '[id="user-menu-button"]'
        self.sign_out_btn = 'input[value="Sign Out"]'

    @step
    def signed_in_alert_has_text(self, expected_text):
        expect(self.page.locator(self.signed_in_alert)).to_have_text(expected_text)
        return self

    @step
    def click_on_user_menu(self):
        self.user_menu_btn.click()
        return self

    @step
    def click_to_sign_out(self):
        self.sign_out_btn.click()
        return self

    @step
    def open_project(self, project):
        s(by.css(f'[title="{project}"]')).click()
        return self

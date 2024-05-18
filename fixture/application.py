from playwright.sync_api import Browser, Page, APIRequestContext

from models.common_test_data import CommonTestData


class Application:
    def __init__(self):
        self.browser: Browser = None
        self.page: Page = None
        self.request_context: APIRequestContext = None
        self.logger = None
        self.env = ""
        self.test_data: CommonTestData = None

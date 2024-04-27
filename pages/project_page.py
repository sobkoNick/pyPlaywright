from playwright.sync_api import Page, expect
from reportportal_client import step


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.account_btn = page.locator('[class="mainnav-menu-footer"] a[href="/account"]')
        self.first_suite_input = page.locator('input[placeholder="First Suite"]')
        self.add_suite_btn = page.locator('//button[text()="Suite"]')
        self.suite_item = '//p[@class="nestedItem-title"]//span[text()="{suite_name}"]'
        self.opened_suite_title = page.locator('[class="detailed-view-suite-body"] h3')
        # Test fragment locators
        self.test_data_frame = 'iframe:nth-child(1)'
        self.file_suite_type = page.locator('li[role="radio"]').locator('nth=0')
        self.add_new_test_btn = page.locator('//a[contains(@href, "/new-test")]')
        self.test_name_input = page.locator('[placeholder="Title"]')
        self.save_test_btn = page.locator('//div[@class="detail-view-actions"]//button')
        self.requirements_input = page.locator('//*[@class="view-line"][2]')
        self.steps_input = page.locator('//*[@class="view-line"][4]')
        self.test_steps = page.locator('(//h3[@id="steps"]/following-sibling::ol)[1]//li')
        self.test_requirements = page.locator('(//h3[@id="requirements"]/following-sibling::ol)[1]//li')

    @step
    def is_account_btn_visible(self) -> bool:
        return self.account_btn.is_visible()

    @step
    def click_on_account_btn(self):
        self.account_btn.click()
        return self

    @step
    def set_suite_name(self, name):
        self.first_suite_input.type(name)
        return self

    @step
    def click_to_add_suite(self):
        self.add_suite_btn.click()
        return self

    @step
    def choose_suite(self, suite_name):
        self.page.locator(self.suite_item.format(suite_name=suite_name)).click()
        return self

    @step
    def verify_opened_suite_title(self, suite_title):
        expect(self.opened_suite_title).to_have_text(suite_title)
        return self

    @step
    def choose_file_suite_type(self):
        self.file_suite_type.click()
        return self

    @step
    def click_to_add_new_test(self):
        self.add_new_test_btn.click()
        return self

    @step
    def set_test_name(self, name):
        self.test_name_input.type(name)
        return self

    @step
    def save_test(self):
        self.save_test_btn.click()
        return self

    @step
    def select_test(self, test_title):
        self.page.locator(f"//div[@class='collection']//a[text()='{test_title}']").click()
        return self

    @step
    def verify_requirements(self, requirements):
        expect(self.test_requirements).to_have_text(requirements)
        return self

    @step
    def verify_steps(self, steps):
        expect(self.test_steps).to_have_text(steps)
        return self

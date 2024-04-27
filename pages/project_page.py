from reportportal_client import step


class ProjectPage:
    def __init__(self):
        self.account_btn = s(by.css('[class="mainnav-menu-footer"] a[href="/account"]'))
        self.first_suite_input = s(by.css('input[placeholder="First Suite"]'))
        self.add_suite_btn = s(by.xpath('//button[text()="Suite"]'))
        self.suite_item = '//p[@class="nestedItem-title"]//span[text()="{suite_name}"]'
        self.opened_suite_title = s(by.css('[class="detailed-view-suite-body"] h3'))
        # Test fragment locators
        self.test_data_frame = s(by.css('iframe:nth-child(1)'))
        self.file_suite_type = s(by.css('li[role="radio"]'))
        self.add_new_test_btn = s(by.xpath('//a[contains(@href, "/new-test")]'))
        self.test_name_input = s(by.css('[placeholder="Title"]'))
        self.save_test_btn = s(by.xpath('//div[@class="detail-view-actions"]//button'))
        self.requirements_input = s(by.xpath('//*[@class="view-line"][2]'))
        self.steps_input = s(by.xpath('//*[@class="view-line"][4]'))
        self.test_steps = ss(by.xpath('(//h3[@id="steps"]/following-sibling::ol)[1]//li'))
        self.test_requirements = ss(by.xpath('(//h3[@id="requirements"]/following-sibling::ol)[1]//li'))

    @step
    def is_account_btn_visible(self) -> bool:
        return self.account_btn.matching(be.visible)

    @step
    def click_on_account_btn(self):
        self.account_btn.click()
        return self

    @step
    def set_suite_name(self, name):
        self.first_suite_input.set(name)
        return self

    @step
    def click_to_add_suite(self):
        self.add_suite_btn.click()
        return self

    @step
    def choose_suite(self, suite_name):
        s(by.xpath(self.suite_item.format(suite_name=suite_name))).click()
        return self

    @step
    def verify_opened_suite_title(self, suite_title):
        self.opened_suite_title.should(have.exact_text(suite_title))
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
        self.test_name_input.set(name)
        return self

    @step
    def set_test_requirements(self, requirements_text):
        self.switch_to_frame()
        # todo this does not work. requirements and test steps are not saved after click on Save.
        script = f"document.querySelector('[class=\"view-line\"]:nth-child(2) span span')" \
                 f".innerText='{requirements_text}'"
        browser.driver.execute_script(script)

        script2 = "document.querySelector('[class=\"view-line\"]:nth-child(2) span span')" \
                  ".setAttribute('class', 'mtk1')"
        browser.driver.execute_script(script2)
        # self.requirements_input.set(requirements_text)
        browser.switch_to.default_content()
        return self

    @step
    def set_test_steps(self, steps_text):
        self.switch_to_frame()
        script = f"document.querySelector('[class=\"view-line\"]:nth-child(4) span span')" \
                 f".textContent='{steps_text}'"
        browser.driver.execute_script(script)

        script2 = "document.querySelector('[class=\"view-line\"]:nth-child(4) span span')" \
                  ".setAttribute('class', 'mtk1')"
        browser.driver.execute_script(script2)

        # self.steps_input.set(steps_text)
        browser.switch_to.default_content()
        return self

    def switch_to_frame(self):
        self.test_data_frame.should(be.visible)
        browser.switch_to.frame(1)

    @step
    def save_test(self):
        self.save_test_btn.click()
        return self

    @step
    def select_test(self, test_title):
        s(by.xpath(f"//div[@class='collection']//a[text()='{test_title}']")).click()
        return self

    @step
    def verify_requirements(self, requirements):
        self.test_requirements.should(have.exact_texts(requirements))
        return self

    @step
    def verify_steps(self, steps):
        self.test_steps.should(have.exact_texts(steps))
        return self

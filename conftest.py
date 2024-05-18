import json
import os
from copy import copy

import pytest
from playwright.sync_api import sync_playwright
from reportportal_client import step

import settings
from api_steps.login_api_client import LoginApiClient
from constants import endpoint_names
from fixture.application import Application
from models.common_test_data import CommonTestData
from pages.home_page import HomePage
from pages.project_page import ProjectPage
from utils.logger import CustomLogger


def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="qa", help="dev or qa"
    )


@pytest.fixture(scope="session")
def app(request):
    global fixture
    fixture = Application()
    fixture.logger = CustomLogger().set_up(__name__)

    fixture.env = request.config.getoption("--env")
    settings.ENV = copy(fixture.env)
    fixture.test_data = load_test_data(fixture.logger)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        fixture.browser = browser
        fixture.page = fixture.browser.new_page()
        yield fixture
        browser.close()


@pytest.fixture(autouse=True)
def logout_after_test(app):
    yield
    project_page = ProjectPage(app.page)
    if project_page.is_account_btn_visible():
        project_page.click_on_account_btn()
    HomePage(app.page).click_on_user_menu().click_to_sign_out()
    app.page.context.clear_cookies()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Attaches a screenshot on Report Portal on test failure
    """
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        fixture.logger.error(f"{rep.head_line} {rep.outcome}",
                             attachment={"name": f"{rep.head_line}.png",
                                         "data": fixture.page.screenshot(full_page=True),
                                         "mime": "image/png"})


@step("Loads test data from file and gets jwt token")
def load_test_data(logger) -> CommonTestData:
    file_path = os.path.join(settings.PROJECT_ROOT, "config/{}_config.json".format(settings.ENV))
    with open(file_path, 'r') as json_data:
        test_data_as_json = json.loads(json_data.read())
        jwt_token = request_and_verify_jwt(logger, test_data_as_json["api_token_to_get_jwt"])
        test_data_as_json["jwt_token"] = jwt_token
        del test_data_as_json["api_token_to_get_jwt"]
        return CommonTestData(**test_data_as_json)


@step("Sends request from fixture to get jwt token")
def request_and_verify_jwt(logger, api_token_to_get_jwt):
    jwt_response = LoginApiClient(endpoint_names.LOGIN_ENDPOINT, logger, api_token_to_get_jwt).get_jwt()
    code = jwt_response.status_code
    jwt_token = jwt_response.json()["jwt"]
    if code != 200 or not jwt_token.strip():
        pytest.skip(f"Unable to get JWT token. Status code - {code}, token - {jwt_token}")
    return jwt_token

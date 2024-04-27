import json

import pystreamapi
from _pytest.fixtures import fixture

from api_steps.api_client import ApiClient
from constants.endpoint_names import SUITES_ENDPOINT
from models.suite_model import Suite
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.project_page import ProjectPage


#   ---FIXTURES---

@fixture(autouse=True)
def perform_login(app):
    """
    Test precondition to perform login
    """
    LoginPage().login(app.test_data.login_url, app.test_data.user_credentials)


suites = ['selene_autotest_suite_1', 'selene_autotest_suite_2']


# Something like data provider. suites -> request.
# 'suites' are used as parameter, but each list item is passed in request.param
@fixture(params=suites)
def suite_name(app, request):
    name = request.param
    yield name

    app.logger.info('Deleting the created suite using API')
    all_suites = ApiClient(token=app.test_data.jwt_token, endpoint=SUITES_ENDPOINT, logger=app.logger) \
        .get([app.test_data.project_id]) \
        .validate_that() \
        .status_code_is_ok() \
        .get_response_as_list_of(Suite)

    found_suite = pystreamapi.Stream.of(all_suites) \
        .filter(lambda suite: suite.attributes.title == name) \
        .find_first()

    if found_suite.is_present():
        ApiClient(token=app.test_data.jwt_token, endpoint=SUITES_ENDPOINT, logger=app.logger) \
            .delete([app.test_data.project_id, found_suite.get().id]) \
            .validate_that().status_code_is_ok()


@fixture
def existing_suite(app):
    with open("tests/test_data/existing_suite.json") as json_data:
        suite_data_to_post = json.load(json_data)

    # creates default suite for tests
    created_suite = ApiClient(token=app.test_data.jwt_token, endpoint=SUITES_ENDPOINT, logger=app.logger) \
        .post(url_params=[app.test_data.project_id], new_obj=suite_data_to_post) \
        .validate_that().status_code_is_ok().get_response_as(Suite)

    # passes suite name
    yield created_suite.attributes.title

    app.logger.info("Deleting existing suite after test run")
    ApiClient(token=app.test_data.jwt_token, endpoint=SUITES_ENDPOINT, logger=app.logger) \
        .delete(url_params=[app.test_data.project_id, created_suite.id]) \
        .validate_that().status_code_is_ok()


#   ---TESTS---

def test_suite_creation(app, suite_name):
    """
    Test creates a new suite, opens it and verifies the name in a title field
    """
    HomePage().open_project(app.test_data.project_name)
    ProjectPage() \
        .set_suite_name(suite_name) \
        .click_to_add_suite() \
        .choose_suite(suite_name) \
        .verify_opened_suite_title(suite_name)


def test_suite_is_present_on_ui(app, existing_suite):
    """
    Test opens existing suite (created using API) and verifies the name in a title field
    """
    HomePage().open_project(app.test_data.project_name)
    ProjectPage() \
        .choose_suite(existing_suite) \
        .verify_opened_suite_title(existing_suite)

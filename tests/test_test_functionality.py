import json
import re

import pytest
from _pytest.fixtures import fixture

from api_steps.api_client import ApiClient
from constants.endpoint_names import SUITES_ENDPOINT, TESTS_ENDPOINT
from models.suite_model import Suite
from models.test_model import Test
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


@fixture
def existing_suite_for_test(app):
    with open("tests/test_data/existing_suite.json") as json_data:
        suite_data_to_post = json.load(json_data)

    # creates default suite for tests
    created_suite = ApiClient(token=app.test_data.jwt_token, endpoint=SUITES_ENDPOINT, logger=app.logger) \
        .post(url_params=[app.test_data.project_id], new_obj=suite_data_to_post) \
        .validate_that().status_code_is_ok() \
        .get_response_as(Suite)

    # passes suite name
    yield created_suite.attributes.title

    app.logger.info("Deleting existing suite after test run")
    ApiClient(token=app.test_data.jwt_token, endpoint=SUITES_ENDPOINT, logger=app.logger) \
        .delete(url_params=[app.test_data.project_id, created_suite.id]) \
        .validate_that().status_code_is_ok()


@fixture
def existing_test(app):
    with open("tests/test_data/existing_suite.json") as json_data:
        suite_data_to_post = json.load(json_data)
    with open("tests/test_data/existing_test.json") as json_data:
        test_data_to_post = json.load(json_data)

    # creates default suite for tests
    created_suite = ApiClient(token=app.test_data.jwt_token, endpoint=SUITES_ENDPOINT, logger=app.logger) \
        .post(url_params=[app.test_data.project_id], new_obj=suite_data_to_post) \
        .validate_that().status_code_is_ok() \
        .get_response_as(Suite)

    test_data_obj = Test(**test_data_to_post['data'])
    test_data_obj.attributes.suite_id = created_suite.id

    # creates default test in suite
    created_test = ApiClient(token=app.test_data.jwt_token, endpoint=TESTS_ENDPOINT, logger=app.logger) \
        .post(url_params=[app.test_data.project_id], new_obj=test_data_obj) \
        .validate_that().status_code_is_ok() \
        .get_response_as(Test)

    test_name = created_test.attributes.title
    description = created_test.attributes.description
    requirements = re.findall(r'\d+\.\s(.*?)\n', re.split('Steps', description)[0])
    steps = re.split(r'\n\d.\s', re.split('Steps', description)[1])
    steps.remove('')

    # passes test arguments
    yield created_suite.attributes.title, test_name, requirements, steps

    app.logger.info("Deleting existing suite after test run")
    ApiClient(token=app.test_data.jwt_token, endpoint=SUITES_ENDPOINT, logger=app.logger) \
        .delete(url_params=[app.test_data.project_id, created_suite.id]) \
        .validate_that().status_code_is_ok()


#   ---TESTS---

@pytest.mark.skip(reason="No way to save test requirements and test steps")
def test_adding_test_case_to_suite(app, existing_suite_for_test):
    """
    Test adds a new test to existing suite and verifies data was saved correctly
    """
    HomePage().open_project(app.test_data.project_name)
    ProjectPage() \
        .choose_suite(existing_suite_for_test) \
        .choose_file_suite_type() \
        .click_to_add_new_test() \
        .set_test_name("created by autotest") \
        .set_test_requirements("req1") \
        .set_test_steps("step1") \
        .save_test()


def test_opening_existing_test(app, existing_test):
    """
    Test opening existing test and verifying fields
    """
    HomePage().open_project(app.test_data.project_name)
    ProjectPage() \
        .choose_suite(existing_test[0]) \
        .choose_file_suite_type() \
        .select_test(existing_test[1]) \
        .verify_requirements(existing_test[2]) \
        .verify_steps(existing_test[3])

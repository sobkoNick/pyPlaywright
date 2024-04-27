import json

from assertpy import assert_that
from reportportal_client import step
from requests import Response


class Validator:
    def __init__(self, response: Response):
        self.response = response

    @step
    def status_code_is_ok(self):
        actual_status_code = self.response.status_code
        assert_that(actual_status_code, f"Actual status code {actual_status_code} is not 200 OK") \
            .is_equal_to(200)
        return self

    @step
    def status_code_is(self, status_code):
        actual_status_code = self.response.status_code
        assert_that(actual_status_code,
                    f"Actual status code {actual_status_code} differs from expected {status_code}") \
            .is_equal_to(status_code)
        return self

    def get_response_body(self):
        return self.response.json()

    def get_response_as(self, clazz):
        return clazz(**self.response.json()['data'])

    def get_response_as_list_of(self, clazz):
        actual_objs = []
        for obj in self.get_response_body()['data']:
            actual_objs.append(clazz(**obj))
        return actual_objs


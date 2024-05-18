from copy import copy

from playwright.sync_api import APIRequestContext
from reportportal_client import step

from api_steps.validator import Validator
from utils import url_maker


# Base class for all API steps classes. These methods can be used directly from tests.
class ApiClient:
    def __init__(self, request_context: APIRequestContext, token="", endpoint="", logger=None):
        self.request_context = request_context
        self.token = token
        self.endpoint = endpoint
        self.response = None
        self.logger = logger

        self.post_url = None
        self.put_url = None
        self.get_url = None
        self.get_by_id_url = None
        self.delete_url = None

        self.get_urls_for_endpoint(endpoint)

    def get_urls_for_endpoint(self, endpoint):
        url_map = url_maker.get_urls(endpoint)
        self.post_url = url_map['post']
        self.put_url = url_map['put']
        self.get_url = url_map['get']
        self.get_by_id_url = url_map['get_by_id']
        self.delete_url = url_map['delete']

    def get_headers(self):
        return {"Authorization": self.token}

    # ------- API CALLS -------

    @step
    def get(self, url_params: list):
        """
        :param url_params: a list with params to format url with
        :return: self
        """
        headers = self.get_headers()
        url = self.get_url.format(*url_params)

        self.response = self.request_context.get(url=url, headers=headers)
        self.log_request("GET", url, headers, None)
        self.log_response(self.response.status, self.response.text())
        return self

    @step
    def get_by_id(self, url_params: list):
        """
        :param url_params: a list with params to format url with. should include id to get
        :return: self
        """
        headers = self.get_headers()
        url = self.get_by_id_url.format(*url_params)

        self.response = self.request_context.get(url=url, headers=headers)
        self.log_request("GET", url, headers, None)
        self.log_response(self.response.status, self.response.text())
        return self

    @step
    def post(self, url_params: list, new_obj):
        """
        :param url_params: a list with params to format url with
        :param new_obj: object to be posted
        :return: self
        """
        headers = self.get_headers()
        url = self.post_url.format(*url_params)

        if type(new_obj) is dict:
            data_to_post = copy(new_obj)
        else:
            data_to_post = {'data': new_obj.dict()}

        self.response = self.request_context.post(url=url, headers=headers, data=data_to_post)
        self.log_request("POST", url, headers, data_to_post)
        self.log_response(self.response.status, self.response.text())
        return self

    @step
    def put(self, url_params: list, obj):
        """
        :param url_params: a list with params to format url with. should include id to update
        :param obj: object to be updated
        :return: self
        """
        headers = self.get_headers()
        url = self.put_url.format(*url_params)

        if type(obj) is dict:
            data_to_put = copy(obj)
        else:
            data_to_put = {'data': obj.dict()}

        self.response = self.request_context.put(url=url, headers=headers, data=data_to_put)
        self.log_request("PUT", url, headers, data_to_put)
        self.log_response(self.response.status, self.response.text())
        return self

    @step
    def delete(self, url_params: list):
        """
        :param url_params: a list with params to format url with. should include id to delete
        :return: self
        """
        headers = self.get_headers()
        url = self.delete_url.format(*url_params)

        self.response = self.request_context.delete(url=url, headers=headers)
        self.log_request("DELETE", url, headers, None)
        self.log_response(self.response.status, self.response.text())
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

    def log_request(self, req_method, url, headers, data):
        curl_command = f"curl -X {req_method} '{url}'"

        # Add headers to the cURL command
        for header, value in headers.items():
            curl_command += f" -H '{header}: {value}'"

        if data:
            curl_command += f" --data-raw '{data}'"

        self.logger.info(f"\ncURL request:\n{curl_command}\n")

    def log_response(self, status, text):
        self.logger.info(f"Response \ncode = {status}\ntext = {text}")

    def validate_that(self) -> Validator:
        """
        Returns validator to check response result
        :rtype: Validator
        """
        return Validator(self.response)

from copy import copy

import curl
import requests
from reportportal_client import step

from api_steps.validator import Validator
from utils import url_maker


# Base class for all API steps classes. These methods can be used directly from tests.
class ApiClient:
    def __init__(self, token="", endpoint="", logger=None):
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

        self.response = requests.get(url=url, headers=headers)
        self.log_request_and_response()
        return self

    @step
    def get_by_id(self, url_params: list):
        """
        :param url_params: a list with params to format url with. should include id to get
        :return: self
        """
        headers = self.get_headers()
        url = self.get_by_id_url.format(*url_params)

        self.response = requests.get(url=url, headers=headers)
        self.log_request_and_response()
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

        self.response = requests.post(url=url, json=data_to_post, headers=headers)
        self.log_request_and_response()
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

        self.response = requests.put(url=url, json=data_to_put, headers=headers)
        self.log_request_and_response()
        return self

    @step
    def delete(self, url_params: list):
        """
        :param url_params: a list with params to format url with. should include id to delete
        :return: self
        """
        headers = self.get_headers()
        url = self.delete_url.format(*url_params)

        self.response = requests.delete(url=url, headers=headers)
        self.log_request_and_response()
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

    # used curl instead in the method below
    # def log_request(self, method, headers, url, body):
    #     self.logger.info(f"{method} url = {url}\nheaders = {headers}\nbody = {body}")

    def log_request_and_response(self):
        self.logger.info(f"Request \n{curl.parse(self.response, print_it=False, return_it=True)}")
        self.logger.info(f"Response \ncode = {self.response.status_code}\ntext = {self.response.text}")

    def validate_that(self) -> Validator:
        """
        Returns validator to check response result
        :rtype: Validator
        """
        return Validator(self.response)

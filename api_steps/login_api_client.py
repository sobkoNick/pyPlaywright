import curl
import requests
from reportportal_client import step
from requests import Response

from api_steps.api_client import ApiClient


class LoginApiClient(ApiClient):
    def __init__(self, endpoint, logger, api_token):
        self.api_token = api_token
        super().__init__(endpoint=endpoint, logger=logger)

    @step
    def get_jwt(self) -> Response:
        response = requests.post(url=self.post_url, params=[("api_token", self.api_token)])
        self.logger.info(f"Request \n{curl.parse(response, print_it=False, return_it=True)}")
        self.logger.info(f"Response \ncode = {response.status_code}\ntext = {response.text}")

        self.response = response
        return response

    def send_jwt_request(self):
        self.get_jwt()
        return self

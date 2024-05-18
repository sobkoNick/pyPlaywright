from playwright.sync_api import APIRequestContext
from reportportal_client import step

from api_steps.api_client import ApiClient


class LoginApiClient(ApiClient):
    def __init__(self, request_context: APIRequestContext, endpoint, logger, api_token):
        self.api_token = api_token
        super().__init__(request_context=request_context, endpoint=endpoint, logger=logger)

    @step
    def get_jwt(self):
        params = {'api_token': self.api_token}
        response = self.request_context.post(url=self.post_url, params=params)
        self.logger.info(f"Response \ncode = {response.status}\ntext = {response.text}")

        self.response = response
        return response.json(), response.status

    def send_jwt_request(self):
        self.get_jwt()
        return self

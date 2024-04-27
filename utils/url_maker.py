import os

import jsonpickle

from settings import PROJECT_ROOT
from utils.config_util import get_config

json_file = os.path.join(PROJECT_ROOT, "config/url_constants.json")
with open(json_file) as jfile:
    jsonList = jsonpickle.decode(jfile.read())


def get_urls(endpoint):
    """
    Get needed urls for service using endpoint parameter
    @param endpoint: Service name
    @return: map of urls that will be used in requests
    """
    post_url = ""
    put_url = ""
    get_url = ""
    get_by_id_url = ""
    delete_url = ""

    for item in jsonList:
        if item["endpoint"] == endpoint:
            if "post" in item["urls"]:
                post_url = item["urls"]["post"]
            if "put" in item["urls"]:
                put_url = item["urls"]["put"]
            if "get" in item["urls"]:
                get_url = item["urls"]["get"]
            if "get_by_id" in item["urls"]:
                get_by_id_url = item["urls"]["get_by_id"]
            if "delete" in item["urls"]:
                delete_url = item["urls"]["delete"]

    base_url = get_config("base_url")
    return {"post": base_url + post_url, "put": base_url + put_url, "get": base_url + get_url,
            "get_by_id": base_url + get_by_id_url, "delete": base_url + delete_url}

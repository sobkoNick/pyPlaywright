import os

from config import config_from_json

import settings
from settings import PROJECT_ROOT


def get_config(property_name):
    json_file = os.path.join(PROJECT_ROOT, "config/{}_config.json".format(settings.ENV))
    return config_from_json(json_file, read_from_file=True)[property_name]

# Using jsonpickle
#
# with open(json_file) as jfile:
#     jsonList = jsonpickle.decode(jfile.read())
#
#
# def get_config(property_name):
#     return jsonList[property_name]

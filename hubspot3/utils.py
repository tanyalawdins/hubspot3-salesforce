"""
base utils for the hubspot3 library
"""
import logging

import requests

from hubspot3.globals import BASE_URL


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


def get_log(name):
    logger = logging.getLogger(name)
    logger.addHandler(NullHandler())
    return logger


def auth_checker(access_token: str) -> int:
    """Do a simple api request using the access token"""
    url = "{}/contacts/v1/lists/all/contacts/all?count=1&offset=0&access_token={}".format(
        BASE_URL, access_token
    )
    result = requests.get(url)
    return result.status_code


def force_utf8(raw):
    """Will force the string to convert to valid utf8"""
    string = raw
    try:
        string = string.decode("utf-8", "ignore")
    except Exception:
        pass
    return string


def prettify(obj_with_props, id_key):
    prettified = {
        prop: obj_with_props["properties"][prop]["value"]
        for prop in obj_with_props["properties"]
    }
    prettified["id"] = obj_with_props[id_key]
    try:
        prettified.update(
            {
                assoc: obj_with_props["associations"][assoc]
                for assoc in obj_with_props["associations"]
            }
        )
    except KeyError:
        pass

    return prettified

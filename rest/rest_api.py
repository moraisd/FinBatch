import logging

import requests
from requests import Response


def get_data_dec(func):
    def inner(url):
        return get_data(func(url))

    return inner


def get_data(url) -> Response:
    log = logging.getLogger(__name__)
    log.info(url)
    headers = {'Accept': '*/*'}

    return requests.get(url, headers=headers, timeout=6)

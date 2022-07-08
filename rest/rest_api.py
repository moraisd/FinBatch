import logging

import requests
from requests import Response


def get_data(url) -> Response:
    log = logging.getLogger(__name__)
    log.info(url)
    headers = {'Accept': '*/*'}

    return requests.get(url, headers=headers, timeout=6)

import logging

import requests
from requests import Response


class RestApi:

    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        super().__init__()

    def request_get_data(self, url) -> Response:
        self.log.info(url)
        headers = {'Accept': '*/*'}

        return requests.get(url, headers=headers, timeout=6)

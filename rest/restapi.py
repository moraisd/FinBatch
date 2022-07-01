import logging

import requests
from requests import Response, Timeout, RequestException


class RestApi:

    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        super().__init__()

    def request_get_data(self, url) -> Response:
        self.log.info(url)
        headers = {'Accept': '*/*'}

        try:
            return requests.get('https://httpstat.us/200?sleep=10000', headers=headers, timeout=6)
        except Timeout:
            self.log.warning(f'Connection to {url} timed out:', exc_info=True)
        except RequestException:
            self.log.warning(f'Connection to {url} failed:', exc_info=True)

        return Response()

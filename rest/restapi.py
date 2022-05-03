import requests
from requests import Response


class RestApi:

    def request_get_data(self, url) -> Response:
        print(url)
        headers = {'Accept': '*/*'}

        # TODO Implement timeout feature
        return requests.get(url, headers=headers)

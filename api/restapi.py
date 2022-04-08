import requests


class RestApi:

    def request_get_data(self, url):
        print(url)
        headers = {'Accept': '*/*'}

        return requests.get(url, headers=headers)

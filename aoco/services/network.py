from typing import Any

import requests


class NetworkService:
    @staticmethod
    def get(url: str, data: Any = None, cookies: Any = None, as_json: bool = True):
        response = requests.get(url, data=data, cookies=cookies)
        return response.json() if as_json else response.text

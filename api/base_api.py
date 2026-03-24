import os
import requests
from dotenv import load_dotenv

load_dotenv("/shared/.env", override=True)
load_dotenv(override=False)

class BaseAPI:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL").rstrip("/")
        self.consumer_key = os.getenv("CONSUMER_KEY")
        self.consumer_secret = os.getenv("CONSUMER_SECRET")
        self.headers = {"Content-Type": "application/json"}

    def _build_url(self, endpoint: str) -> str:
        endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{endpoint}"

    def post(self, endpoint, data, params=None):
        return requests.post(
            self._build_url(endpoint),
            json=data,
            params=params,
            headers=self.headers,
            auth=(self.consumer_key, self.consumer_secret)
        )

    def get(self, endpoint, params=None):
        return requests.get(
            self._build_url(endpoint),
            params=params,
            headers=self.headers,
            auth=(self.consumer_key, self.consumer_secret)
        )

    def put(self, endpoint, data, params=None):
        return requests.put(
            self._build_url(endpoint),
            json=data,
            params=params,
            headers=self.headers,
            auth=(self.consumer_key, self.consumer_secret)
        )

    def delete(self, endpoint, params=None):
        return requests.delete(
            self._build_url(endpoint),
            params=params,
            headers=self.headers,
            auth=(self.consumer_key, self.consumer_secret)
        )
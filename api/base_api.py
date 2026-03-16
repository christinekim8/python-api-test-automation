import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file, overriding any existing values
load_dotenv(override=True)

class BaseAPI:
    """
    Base API class to handle common HTTP requests and authentication.
    All specific API classes (e.g., ProductsAPI) will inherit from this.
    """

    def __init__(self):
        self.base_url = os.getenv("BASE_URL").rstrip("/")  # e.g. http://localhost:8000/wp-json/wc/v3
        self.consumer_key = os.getenv("CONSUMER_KEY")
        self.consumer_secret = os.getenv("CONSUMER_SECRET")

        self.headers = {"Content-Type": "application/json"}

    def _use_wp_app_password(self) -> bool:
        """
        If CONSUMER_KEY/CONSUMER_SECRET are not WooCommerce ck_/cs_ keys, treat them as
        WordPress username + Application Password and use HTTP Basic Auth.
        """
        if not self.consumer_key or not self.consumer_secret:
            return False
        return not (self.consumer_key.startswith("ck_") and self.consumer_secret.startswith("cs_"))

    def _build_url(self, endpoint: str) -> str:
        # Avoid double slashes; allow endpoints with or without leading slash
        endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{endpoint}"

    def _with_auth_params(self, extra_params: dict | None = None) -> dict:
        if self._use_wp_app_password():
            return extra_params or {}

        params = {
            "consumer_key": self.consumer_key,
            "consumer_secret": self.consumer_secret,
        }
        if extra_params:
            params.update(extra_params)
        return params

    def post(self, endpoint, data, params=None):
        """Standard POST request for resource creation."""
        url = self._build_url(endpoint)
        all_params = self._with_auth_params(params)
        auth = (self.consumer_key, self.consumer_secret) if self._use_wp_app_password() else None
        response = requests.post(url, json=data, params=all_params, headers=self.headers, auth=auth)
        return response

    def get(self, endpoint, params=None):
        """Standard GET request for resource retrieval."""
        url = self._build_url(endpoint)
        all_params = self._with_auth_params(params)
        auth = (self.consumer_key, self.consumer_secret) if self._use_wp_app_password() else None
        response = requests.get(url, params=all_params, headers=self.headers, auth=auth)
        return response

    def put(self, endpoint, data, params=None):
        """Standard PUT request for resource updates."""
        url = self._build_url(endpoint)
        all_params = self._with_auth_params(params)
        auth = (self.consumer_key, self.consumer_secret) if self._use_wp_app_password() else None
        response = requests.put(url, json=data, params=all_params, headers=self.headers, auth=auth)
        return response

    def delete(self, endpoint, params=None):
        """Standard DELETE request for resource removal."""
        url = self._build_url(endpoint)
        all_params = self._with_auth_params(params)
        auth = (self.consumer_key, self.consumer_secret) if self._use_wp_app_password() else None
        response = requests.delete(url, params=all_params, headers=self.headers, auth=auth)
        return response
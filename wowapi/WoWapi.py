import os
import requests
import datetime
import logging

# Create a logger for this module
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class WoWAPI:
    def __init__(self, region="us"):
        self.access_token = self._get_access_token()
        self.region = region
        self.base_url = f"https://{region}.api.blizzard.com"

    def _get_access_token(self):
        token = os.getenv("BNET_ACCESS_TOKEN")
        if not token:
            raise Exception("Blizzard API access token not found in environment variables.")
        return token

    def _make_request(self, endpoint, params=None):
        if params is None:
            params = {}
        params['access_token'] = self.access_token
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_ah_commodities_data(self, namespace="dynamic-us"):
        endpoint = "/data/wow/auctions/commodities"
        params = {
            "namespace": namespace,
            "locale": "en_US",
        }
        return self._make_request(endpoint, params)

    def get_item_data(self, item_id):
        endpoint = f"/data/wow/item/{item_id}"
        params = {
            "namespace": "static-us",
            "locale": "en_US",
        }
        return self._make_request(endpoint, params)

    def get_item_media(self, item_id):
        endpoint = f"/data/wow/media/item/{item_id}"
        params = {
            "namespace": "static-us",
            "locale": "en_US",
        }
        return self._make_request(endpoint, params)

    def search_item_by_name(self, item_name, page=1):
        endpoint = "/data/wow/search/item"
        params = {
            "namespace": "static-us",
            "name.en_US": item_name,
            "orderby": "name",
            "_pageSize": 50,
            "_page": page,
        }
        data = self._make_request(endpoint, params)
        if data["results"]:
            return data["results"]
        else:
            raise Exception("Item not found.")

    @staticmethod
    def add_timestamp(item_data):
        item_data["ts"] = datetime.datetime.now(datetime.timezone.utc)
        return item_data
    
    @staticmethod
    def log_test():
        logger.info("Hello World")
        logger.error("Hello World")
        logger.debug("Hello World")
        logger.warning("Hello World")
        logger.critical("Hello World")

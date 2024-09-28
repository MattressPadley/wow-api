import os
import requests
import datetime
import logging


# Create a logger for this module
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class WoWAPI:
    """
    A class to interact with the World of Warcraft API.

    This class provides methods to retrieve various data from the WoW API,
    including auction house commodities, item data, and item media.
    """

    def __init__(self, region="us"):
        """
        Initialize the WoWAPI instance.

        Args:
            region (str, optional): The region for API requests. Defaults to "us".
        """
        self.access_token = self._get_access_token()
        self.region = region
        self.base_url = f"https://{region}.api.blizzard.com"
        logger.info(f"WoWAPI initialized for region: {region}")

    def _get_access_token(self):
        """
        Retrieve the Blizzard API access token from environment variables.

        Returns:
            str: The access token.

        Raises:
            Exception: If the access token is not found in environment variables.
        """
        token = os.getenv("BNET_ACCESS_TOKEN")
        if not token:
            logger.error("Blizzard API access token not found in environment variables.")
            raise Exception("Blizzard API access token not found in environment variables.")
        logger.debug("Access token retrieved successfully")
        return token

    def _make_request(self, endpoint, params=None):
        """
        Make a request to the Blizzard API.

        Args:
            endpoint (str): The API endpoint to request.
            params (dict, optional): Additional parameters for the request. Defaults to None.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.HTTPError: If the request fails.
        """
        if params is None:
            params = {}
        params['access_token'] = self.access_token
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Making API request to: {url}")
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            logger.debug(f"API request successful: {url}")
            return response.json()
        except requests.HTTPError as e:
            logger.error(f"API request failed: {url}. Error: {str(e)}")
            raise

    def get_ah_commodities_data(self, namespace="dynamic-us"):
        """
        Retrieve auction house commodities data.

        Args:
            namespace (str, optional): The namespace for the request. Defaults to "dynamic-us".

        Returns:
            dict: The auction house commodities data.
        """
        logger.info("Retrieving auction house commodities data")
        endpoint = "/data/wow/auctions/commodities"
        params = {
            "namespace": namespace,
            "locale": "en_US",
        }
        return self._make_request(endpoint, params)

    def get_item_data(self, item_id):
        """
        Retrieve data for a specific item.

        Args:
            item_id (int): The ID of the item to retrieve.

        Returns:
            dict: The item data.
        """
        logger.info(f"Retrieving data for item ID: {item_id}")
        endpoint = f"/data/wow/item/{item_id}"
        params = {
            "namespace": "static-us",
            "locale": "en_US",
        }
        return self._make_request(endpoint, params)

    def get_item_media(self, item_id):
        """
        Retrieve media information for a specific item.

        Args:
            item_id (int): The ID of the item to retrieve media for.

        Returns:
            dict: The item media data.
        """
        logger.info(f"Retrieving media for item ID: {item_id}")
        endpoint = f"/data/wow/media/item/{item_id}"
        params = {
            "namespace": "static-us",
            "locale": "en_US",
        }
        return self._make_request(endpoint, params)

    def search_item_by_name(self, item_name, page=1):
        """
        Search for items by name.

        Args:
            item_name (str): The name of the item to search for.
            page (int, optional): The page number for paginated results. Defaults to 1.

        Returns:
            list: A list of items matching the search criteria.

        Raises:
            Exception: If no items are found.
        """
        logger.info(f"Searching for item: {item_name} (page {page})")
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
            logger.debug(f"Found {len(data['results'])} results for item: {item_name}")
            return data["results"]
        else:
            logger.warning(f"No items found for search: {item_name}")
            raise Exception("Item not found.")

    @staticmethod
    def add_timestamp(item_data):
        """
        Add a timestamp to item data.

        Args:
            item_data (dict): The item data to add a timestamp to.

        Returns:
            dict: The item data with an added timestamp.
        """
        logger.debug("Adding timestamp to item data")
        item_data["ts"] = datetime.datetime.now(datetime.timezone.utc)
        return item_data
    
    @staticmethod
    def log_test():
        """
        Test logging at various levels.
        """
        logger.info("Hello World")
        logger.error("Hello World")
        logger.debug("Hello World")
        logger.warning("Hello World")
        logger.critical("Hello World")


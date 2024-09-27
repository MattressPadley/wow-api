from wowapi import WoWAPI
from pymongo import MongoClient
from prettytable import PrettyTable

# ... (keep your existing imports and other classes)

class BlizzardAPI:
    def __init__(self, region="us"):
        self.api = WoWAPI(region)

    def get_item_data(self, item_id):
        return self.api.get_item_data(item_id)

    def get_item_media(self, item_id):
        return self.api.get_item_media(item_id)

    def search_item_by_name(self, item_name, page=1):
        return self.api.search_item_by_name(item_name, page)

# ... (keep the rest of your code unchanged)

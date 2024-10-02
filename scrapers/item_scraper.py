import logging
from wowapi.WoWapi import WoWAPI
from dotenv import load_dotenv
from pylog import get_logger
from pymongo import MongoClient

# MongoDB connection setup
mongo_client = MongoClient("mongodb://localhost:27017")
db = mongo_client["wow"]
profession_collection = db["professions"]
recipe_collection = db["recipes"]
item_collection = db["items"]

load_dotenv()

api_logger = get_logger(
    "wowapi.WoWapi",
    console=False,
    file=False,
    mongo_uri="mongodb://localhost:27018",
    mongo_db_name="logs",
    mongo_collection_name="testing",
    log_level=logging.DEBUG,
    app_name="Scraper",
)

scraper_logger = get_logger(
    "scraper",
    console=True,
    file=False,
    mongo_uri="mongodb://localhost:27018",
    mongo_db_name="logs",
    mongo_collection_name="testing",
    log_level=logging.DEBUG,
    app_name="Scraper",
)

api = WoWAPI()


    
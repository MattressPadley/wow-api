import os
from pylog import get_logger
from dotenv import load_dotenv
from wowapi import WoWAPI


load_dotenv()

get_logger("wowapi.WoWapi", 
            local_mongo_uri="mongodb://localhost:27017", 
            local_db_name="logs", 
            local_collection_name="testing"
            )

wowapi = WoWAPI()
wowapi.log_test()

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import firebase_admin
import firebase_admin.db
from itemadapter import ItemAdapter
from pathlib import Path
from scrapy.exceptions import DropItem
import os

class OpscrapperPipeline:
    
    def __init__(self):
        #service=Path(__file__).parent
        #service_path_json= service/'manga-scrapy-firebase-adminsdk-p41zm-04853ada62.json'
        service_path_json=os.getenv("FIREBASE_CREDENTIALS_PATH")
        firebase_cred_dict = json.loads(service_path_json)
        cred=firebase_admin.credentials.Certificate(firebase_cred_dict)
        firebase_admin.initialize_app(cred, {
            'databaseURL': os.getenv("FIREBASE_DB_URI")
        })
    def process_item(self, item, spider):
        ref=firebase_admin.db.reference('manga_data')
        try:
            ref.update(dict(item))
            return item
        except Exception as e:
            raise DropItem(f"Failed to push data cuz of : {e}")
        

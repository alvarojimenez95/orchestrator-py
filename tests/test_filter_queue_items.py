
from orchestrator.orchestrator import Orchestrator
import datetime
import logging
from dotenv import load_dotenv
import os
from pprint import pprint
import json
import logging


logging.basicConfig(filename="test.log", filemode="w", level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
TENANT_NAME = os.getenv('TENANT_NAME')
FOLDER_ID = os.getenv('FOLDER_ID')
QUEUE_ID = os.getenv('QUEUE_ID')
ITEM_ID = os.getenv('ITEM_ID')
PRE_FOLDER_ID = os.getenv('PRE_FOLDER_ID')
PROD_FOLDER_ID = os.getenv('PROD_FOLDER_ID')
MACHINE_IDENTIFIER = os.getenv('MACHINE_IDENTIFIER')
print(PROD_FOLDER_ID)

client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
# print(client)
# pprint(client.get_folder_ids())
folder = client.get_folder_by_id(int(PRE_FOLDER_ID))
print("folder found")
queue = folder.get_queue_by_id(127484)
print(queue.name)
print("queue found")
# filt_options = {
#     "$select": "SpecificContent/integration_id"
# }
# items = queue.get_queue_items()
# print("items filtered")
# pprint(len(items))
# pprint(items[0].content())


items = queue.filter_by_reference(reference="integration_id", num_days=2)
pprint(len(items))

# DAYS_DIFF = 4

# today = datetime.datetime.now()
# str_date = "2022-06-24T11:36:13.973Z"
# diff = today - datetime.timedelta(days=datetime.datetime.strptime(str_date, '%Y-%m-%dT%H:%M:%S.%fZ').day)
# print(f"the diff day is {diff.day}")
# if diff.day <= DAYS_DIFF:
#     print("add it")
# else:
#     print("do not add")
# print(diff)

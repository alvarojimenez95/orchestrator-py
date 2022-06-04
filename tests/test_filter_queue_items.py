
from orchestrator.orchestrator import Orchestrator
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
queue = folder.get_queue_by_id(116803)
print(queue.name)
print("queue found")
filt_options = {
    "$filter": "Status in ('Failed', 'Successful')"
}
items = queue.get_queue_items(options=filt_options)
print("items filtered")
pprint(len(items))
# for item in items:
#     item.delete()
# for item in items:
#     queue.start(machine_identifier=MACHINE_IDENTIFIER, specific_content=item.specific_content, reference="key_id")
#     item.delete()
# res = queue.check_duplicate(reference="127101069#6a224d58-eb4b-4fcc-98c9-c644ca4a8302")
# need to pass part of the reference as key
# filt = queue.get_queue_items(options={"$filter": "contains(Reference,'127101069')"})
# print(filt[0].specific_content)

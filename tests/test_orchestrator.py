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
print(PROD_FOLDER_ID)

client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
# print(client)
# pprint(client.get_folder_ids())
folder = client.get_folder_by_id(int(PRE_FOLDER_ID))
client.get_folder_by_id(int(PRE_FOLDER_ID))
client.get_folder_by_id(int(PRE_FOLDER_ID))
folder2 = client.get_folder_by_id(int(PRE_FOLDER_ID))
client.get_folder_by_id(int(PRE_FOLDER_ID))
client.get_folder_by_id(int(PRE_FOLDER_ID))
print("Orchestrator access token is " + str(client.access_token))
client.get_machines()
# print(client._access_token)
client.get_folder_by_id(int(PRE_FOLDER_ID))
queue = folder.get_queue_by_id(116803)
print("Queue access token is " + str(queue.access_token))

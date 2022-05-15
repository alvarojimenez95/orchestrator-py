from orchestrator.orchestrator import Orchestrator

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

# queue = folder.get_queue_by_id(113663)

sp_content1 = {
    "nombre": "Alvaro",
    "edad": "26"
}

hola = "test"

# sp_content2 = {
#     "nombre": "Pedro",
#     "edad": "24"
# }

# sp_contents = [sp_content1, sp_content2]
# queue.bulk_create_items(specific_contents=sp_contents, progress="High")

# alvaro = client.get_machine_by_id(123680)
# pprint(alvaro.info())


queue = folder.get_queue_by_id(113663)
queue.start(machine_identifier="635a3c6d-ff3d-4b58-9a50-a2796257f4c5", specific_content=sp_content1)

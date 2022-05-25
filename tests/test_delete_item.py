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
MACHINE_IDENTIFIER = os.getenv('MACHINE_IDENTIFIER')

print(PROD_FOLDER_ID)

client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
folder = client.get_folder_by_id(int(PRE_FOLDER_ID))
queue = folder.get_queue_by_id(116803)
item_content = {
    "Name": "Yo",
    "Apellido": "Test"
}
# print("Empezando la transaccion")
# res = queue.start(machine_identifier=MACHINE_IDENTIFIER, specific_content=item_content, reference="Name", fields={"doc_type": "updated contract"})
# check = queue.check_duplicate(reference="127101069")
# print(check.specific_content)
item = queue.get_queue_items()[0]
print(item.id)
print(item.content())
item.delete()

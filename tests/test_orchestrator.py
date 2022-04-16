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
FOLDER_PRE_ID = os.getenv('FOLDER_PRE_ID')
PROD_FOLDER_ID = os.getenv('PROD_FOLDER_ID')
print(PROD_FOLDER_ID)

client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
print(client)
pprint(client.get_folder_ids())
folder = client.get_folder_by_id(int(FOLDER_ID))
print(client)
production = client.get_folder_by_id(int(PROD_FOLDER_ID))
print(client)
queues = production.get_all_assets()
# def test_init():
#     client = Orchestrator(client_id=CLIENT_ID,
#                           refresh_token=REFRESH_TOKEN)
#     print(client._access_token)
#     client._get_token()


# def test_folder():
#     """
#     Gets a list of all folders
#     """
#     client = Folder(client_id=CLIENT_ID,
#                     refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
#     data = client.get_all_folders()
#     pprint(data)


# def test_create_item():
#     client = Queue(client_id=CLIENT_ID,
#                    refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
#     hiring = {
#         "name": "Pepa",
#         "surname": "Perez"
#     }
#     specific_content = {
#         "prenom": "Perez",
#         "nom": "Pepe",
#         "anael_id": "12345",
#         "hiring_data": json.dumps(hiring)
#     }
#     data = client.create_queue_item(100093, specific_content=specific_content)
#     pprint(data)


# def test_create_items():
#     client = Queue(client_id=CLIENT_ID,
#                    refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
#     hiring = {
#         "name": "Pepa",
#         "surname": "Perez"
#     }
#     specific_content1 = {
#         "prenom": "Perez",
#         "nom": "Pepe",
#         "anael_id": "12345",
#         "hiring_data": json.dumps(hiring)
#     }
#     specific_content2 = {
#         "prenom": "Perez",
#         "nom": "Antonio",
#         "anael_id": "12345",
#         "hiring_data": json.dumps(hiring)
#     }
#     data = client.bulk_create_items(100093, specific_contents=[specific_content1, specific_content2])
#     pprint(data)

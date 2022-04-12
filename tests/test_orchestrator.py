from orchestrator.orchestrator import Orchestrator, Folder, Queue, Asset

from dotenv import load_dotenv
import os
from pprint import pprint
import json

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
TENANT_NAME = os.getenv('TENANT_NAME')
FOLDER_ID = os.getenv('FOLDER_ID')
QUEUE_ID = os.getenv('QUEUE_ID')
ITEM_ID = os.getenv('ITEM_ID')
FOLDER_PRE_ID = os.getenv('FOLDER_PRE_ID')


def test_init():
    client = Orchestrator(client_id=CLIENT_ID,
                          refresh_token=REFRESH_TOKEN)
    print(client._access_token)
    client._get_token()


def test_folder():
    """
    Gets a list of all folders
    """
    client = Folder(client_id=CLIENT_ID,
                    refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    data = client.get_all_folders()
    pprint(data)


def test_folder_list():
    """
    List of dictionaries folder_name - folder_id
    """
    client = Folder(client_id=CLIENT_ID,
                    refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    data = client.get_folder_ids()
    pprint(data)


def test_single_folder():
    """
    Returns a single folder
    """
    client = Folder(client_id=CLIENT_ID,
                    refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    data = client.get_folder(folder_id=FOLDER_ID)
    pprint(data)


def test_queues_ids():
    """
     List of dictionaries queue_name - queue_id
    """
    client = Queue(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    data = client.get_queue_ids()
    pprint(data)


def test_queues():
    """
        Returns a list of all queues
    """
    client = Queue(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    data = client.get_all_queues(options={"$top": "2", "$orderby": "Id asc"})
    pprint(data)
    # print(queue_ids)


def test_single_queue():
    """
        Gets a single queue by id
    """
    client = Queue(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    data = client.get_queue(QUEUE_ID)
    pprint(data)


def test_queue_processing_recrods():
    """
        Gets all processing records for a given queue id
    """
    client = Queue(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    data = client.get_processing_records(queue_id=QUEUE_ID, num_days=30)
    pprint(data)


def test_processing_recrods():
    """
        Gets all processing records
    """
    client = Queue(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    data = client.get_queue_processing_records()
    pprint(data)
    pprint(len(data))


def test_assets():
    """
        Gets all assets
    """
    client = Asset(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    data = client.get_all_assets()
    pprint(data)


def test_assets_ids():
    """
        Returns a dictionary asset_name -- asset_id
    """
    client = Asset(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    data = client.get_asset_ids()
    pprint(data)


def test_queue_items():
    """
    Gets all items (allows for options)
    """
    client = Queue(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    data = client.get_items(options={"$filter": "QueueDefinitionId eq 100093", "$top": "2"})
    pprint(data)
    pprint(len(data))


def test_queue_item_ids():
    """
        Returns a list of dictionaries with the
        queue id -- item id
    """
    client = Queue(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    data = client.get_queue_items_ids(QUEUE_ID, options={"$top": "2"})
    pprint(data)


def test_queue_items_by_queue_id():
    """
        Returns a list of items for a given queue id
    """
    client = Queue(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    data = client.get_queue_items(QUEUE_ID, options={"$top": "2"})
    pprint(data)


def test_get_queue_item():
    """
    Gets a queue item by item id
    """
    client = Queue(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    data = client.get_item(item_id=ITEM_ID)

    pprint(data)


def test_create_item():
    client = Queue(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    hiring = {
        "name": "Pepa",
        "surname": "Perez"
    }
    specific_content = {
        "prenom": "Perez",
        "nom": "Pepe",
        "anael_id": "12345",
        "hiring_data": json.dumps(hiring)
    }
    data = client.create_queue_item(100093, specific_content=specific_content)
    pprint(data)


def test_create_items():
    client = Queue(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    hiring = {
        "name": "Pepa",
        "surname": "Perez"
    }
    specific_content1 = {
        "prenom": "Perez",
        "nom": "Pepe",
        "anael_id": "12345",
        "hiring_data": json.dumps(hiring)
    }
    specific_content2 = {
        "prenom": "Perez",
        "nom": "Antonio",
        "anael_id": "12345",
        "hiring_data": json.dumps(hiring)
    }
    data = client.bulk_create_items(100093, specific_contents=[specific_content1, specific_content2])
    pprint(data)


test_create_items()
# ----test-------
test_get_queue_item()
test_queues_ids()
test_folder()
test_single_folder()
test_folder_list()
test_queues()
test_single_queue()
test_processing_recrods()
test_queue_processing_recrods()
test_assets()
test_assets_ids()
test_init()
test_queue_items()
test_queue_items_by_queue_id()
test_queue_item_ids()
test_create_item()
test_create_items()

from orchestrator.orchestrator import Orchestrator, Folder, Queue, Asset
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
TENANT_NAME = os.getenv('TENANT_NAME')
FOLDER_ID = os.getenv('FOLDER_ID')
QUEUE_ID = os.getenv('QUEUE_ID')


def test_init():
    client = Orchestrator(client_id=CLIENT_ID,
                          refresh_token=REFRESH_TOKEN)
    print(client._access_token)
    client._get_token()
    print(client._access_token)

    print(CLIENT_ID)


def test_folder():
    client = Folder(client_id=CLIENT_ID,
                    refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    data = client.get_all_folders()
    pprint(data)


def test_folder_list():
    client = Folder(client_id=CLIENT_ID,
                    refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    data = client.get_folder_ids()
    pprint(data)


def test_single_folder():
    client = Folder(client_id=CLIENT_ID,
                    refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    data = client.get_folder(folder_id=FOLDER_ID)
    pprint(data)


def test_queues():
    client = Queue(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    data = client.get_all_queues(options={"$top": "2", "$orderby": "Id asc"})
    pprint(data)
    # print(queue_ids)


def test_single_queue():
    client = Queue(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    data = client.get_queue(QUEUE_ID)
    pprint(data)


def test_processing_recrods():
    client = Queue(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    data = client.get_processing_records(queue_id=QUEUE_ID, num_days=30)
    pprint(data)


def test_queue_processing_recrods():
    client = Queue(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    data = client.get_queue_processing_records()
    pprint(len(data))


def test_assets():

    client = Asset(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    data = client.get_all_assets()
    pprint(len(data))
    pprint(data)


def test_assets_ids():
    client = Asset(client_id=CLIENT_ID,
                   refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME, folder_id=FOLDER_ID)
    data = client.get_asset_ids()
    pprint(len(data))
    pprint(data)


# test_folder()
# test_single_folder()
# test_queues()
# test_single_queue()
# test_queue_processing_recrods()
# test_assets()
# test_assets_ids()
test_init()

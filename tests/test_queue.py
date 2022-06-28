from orchestrator.orchestrator import Orchestrator
from dotenv import load_dotenv
import os
from pprint import pprint
import pytest

LOCAL_TEST = True

if LOCAL_TEST:
    load_dotenv()
    CLIENT_ID = os.getenv('CLIENT_ID')
    REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
    TENANT_NAME = os.getenv('TENANT_NAME')
    FOLDER_ID = os.getenv('FOLDER_ID')
    QUEUE_ID = os.getenv('QUEUE_ID')
    ITEM_ID = os.getenv('ITEM_ID')
    PRE_FOLDER_ID = os.getenv('PRE_FOLDER_ID')
    PROD_FOLDER_ID = os.getenv('PROD_FOLDER_ID')
else:
    load_dotenv()
    CLIENT_ID = os.environ['CLIENT_ID']
    REFRESH_TOKEN = os.environ['REFRESH_TOKEN']
    TENANT_NAME = os.environ['TENANT_NAME']
    FOLDER_ID = os.environ['FOLDER_ID']
    QUEUE_ID = os.environ['QUEUE_ID']
    ITEM_ID = os.getenvironenv['ITEM_ID']
    PRE_FOLDER_ID = os.environ['PRE_FOLDER_ID']
    PROD_FOLDER_ID = os.environ['PROD_FOLDER_ID']


def test_queue_info():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    queue = client.get_folder_by_id(PRE_FOLDER_ID).get_queue_by_id(127484)
    queue.info()


def test_processing_records():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    queue = client.get_folder_by_id(PRE_FOLDER_ID).get_queue_by_id(127484)
    queue.get_processing_records(num_days=2)


def test_get_queue_items():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    queue = client.get_folder_by_id(PRE_FOLDER_ID).get_queue_by_id(127484)
    queue.get_queue_items()


def test_filter_by_reference():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    queue = client.get_folder_by_id(PROD_FOLDER_ID).get_queue_by_id(127136)
    items = queue.filter_by_reference(reference="integration_id", num_days=2)
    print(len(items))
    for item in items:
        assert item[2] in {"Failed", "Retried", "Successful"}


test_filter_by_reference()


def test_get_items_by_status():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    queue = client.get_folder_by_id(PRE_FOLDER_ID).get_queue_by_id(127484)
    items = queue.get_queue_items_by_status(status="Successful")
    for item in items:
        item_atr = item.__dict__
        assert item_atr["folder_id"] == int(PRE_FOLDER_ID)
        assert item_atr["folder_name"]
        assert item_atr["tenant_name"]
        assert item_atr["access_token"]
        assert item_atr["client_id"]
        assert item_atr["queue_id"] == 127484
        assert item_atr["queue_name"]
        assert item_atr["id"]
        assert item_atr["status"] == "Successful"


def test_get_queue_item_ids():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    queue = client.get_folder_by_id(PRE_FOLDER_ID).get_queue_by_id(127484)
    item_ids = queue.get_queue_items_ids()
    assert item_ids


def test_get_queue_item_by_id():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    queue = client.get_folder_by_id(PRE_FOLDER_ID).get_queue_by_id(127484)
    item = queue.get_item_by_id(276927010)
    item_atr = item.__dict__
    assert item_atr["specific_content"]
    assert item_atr["client_id"]
    assert item_atr["access_token"]
    assert item_atr["status"]
    assert item_atr["reference"]
    assert item_atr["tenant_name"]
    assert item_atr["folder_id"]
    assert item_atr["folder_name"]
    assert item_atr["queue_name"]
    assert item_atr["queue_id"]
    assert item_atr["id"]
    print(item)


def test_add_queue_item():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    queue = client.get_folder_by_id(PRE_FOLDER_ID).get_queue_by_id(127129)
    sp_content = {
        "Name": "Alvaro",
        "Surname": "Jimenez"
    }
    item = queue.add_queue_item(specific_content=sp_content)
    assert item.id
    assert item.client_id
    assert item.refresh_token
    assert item.tenant_name
    assert item.status
    assert item.reference
    assert item.folder_id == int(PRE_FOLDER_ID)
    assert item.folder_name
    assert item.queue_name
    assert item.queue_id == 127129


def test_bulk_add_queue_items():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    queue = client.get_folder_by_id(PRE_FOLDER_ID).get_queue_by_id(127129)
    sp_content1 = {
        "Name": "Alvaro",
        "Surname": "Jimenez"
    }
    sp_content2 = {
        "Name": "John",
        "Surname": "Doe"
    }
    data_ref = queue.bulk_create_items(specific_contents=[sp_content1, sp_content2], reference="Name")
    data = queue.bulk_create_items(specific_contents=[sp_content1, sp_content2])
    assert data_ref["Success"]
    assert data["Success"]

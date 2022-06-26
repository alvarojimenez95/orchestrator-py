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
    MACHINE_IDENTIFIER = os.getenv('MACHINE_IDENTIFIER')
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


def test_queue_item_info():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    item = client.get_folder_by_id(PRE_FOLDER_ID).get_queue_by_id(127484).get_item_by_id(276927010)
    item.info()
    item.history()
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


def test_item_last_entry():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    item = client.get_folder_by_id(PRE_FOLDER_ID).get_queue_by_id(127129).get_item_by_id(278271841)
    data = item.last_entry()
    assert data


def test_delete_queue_item():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    queue = client.get_folder_by_id(PRE_FOLDER_ID).get_queue_by_id(127129)
    sp_content = {
        "Name": "Alvaro",
        "Surname": "Jimenez"
    }
    item = queue.add_queue_item(specific_content=sp_content)
    assert item.id
    assert item.folder_id == int(PRE_FOLDER_ID)
    assert item.folder_name
    assert item.queue_id
    assert item.queue_name
    assert item.tenant_name
    assert item.client_id
    assert item.status
    item.delete()


def test_edit_queue_item():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    queue = client.get_folder_by_id(PRE_FOLDER_ID).get_queue_by_id(127129)
    sp_content = {
        "Name": "Alvaro",
        "Surname": "Jimenez"
    }
    item = queue.add_queue_item(specific_content=sp_content)
    assert item.id
    assert item.folder_id == int(PRE_FOLDER_ID)
    assert item.folder_name
    assert item.queue_id
    assert item.queue_name
    assert item.tenant_name
    assert item.client_id
    assert item.status
    body = {
        "Name": item.queue_name,
        "SpecificContent": {
            "Nombre": "Alvaro",
            "Apelllido": "Doe"
        }
    }
    item.edit(body=body)


def test_progress_update():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    queue = client.get_folder_by_id(PRE_FOLDER_ID).get_queue_by_id(127129)
    sp_content = {
        "Name": "Alvaro",
        "Surname": "Jimenez"
    }
    item1 = queue.start(machine_identifier=MACHINE_IDENTIFIER, specific_content=sp_content)
    item2 = queue.start(machine_identifier=MACHINE_IDENTIFIER, specific_content=sp_content, references=["Name"])

    item1.set_transaction_progress(status="This is a test for endpoint SetTransactionProgress")
    item1.set_transaction_status(success=True)

    item2.set_transaction_status(success=False, reason="Failure Test", details="BRE0 - Missing parameters", exception_type="BusinessException")
    item1.delete()
    item2.delete()

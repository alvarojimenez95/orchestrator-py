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

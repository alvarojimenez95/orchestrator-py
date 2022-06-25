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


def test_process_info():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    process = client.get_folder_by_id(PRE_FOLDER_ID).get_process_by_key("BOT_048_FR_PQ_AnaelIntegration:1.0.2-alpha.59")
    process.info()


def test_process_versions():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    process = client.get_folder_by_id(PRE_FOLDER_ID).get_process_by_key("BOT_048_FR_PQ_AnaelIntegration:1.0.2-alpha.59")
    process.versions()


def test_process_parameters():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    process = client.get_folder_by_id(PRE_FOLDER_ID).get_process_by_key("BOT_048_FR_PQ_AnaelIntegration:1.0.2-alpha.59")
    process.parameters()

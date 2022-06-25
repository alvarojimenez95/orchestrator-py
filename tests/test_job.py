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
    job = client.get_folder_by_id(PRE_FOLDER_ID).get_job_by_key("507491b2-8ec3-48d8-b651-cd2a225f51dd")
    job.info()


def test_process_logs():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    job = client.get_folder_by_id(PRE_FOLDER_ID).get_job_by_key("507491b2-8ec3-48d8-b651-cd2a225f51dd")
    logs = job.get_logs()
    for log in logs:
        log_atr = log.__dict__
        assert log_atr["tenant_name"]
        assert log_atr["folder_id"]
        assert log_atr["folder_name"]
        assert log_atr["key"]
        assert log_atr["message"]
        assert log_atr["timestamp"]
        assert log_atr["trace"] in {"Info", "Error"}

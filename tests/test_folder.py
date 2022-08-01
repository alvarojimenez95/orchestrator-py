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
    REFRESH_TOKEN2 = os.getenv('REFRESH_TOKEN2')

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


def test_folder_processes():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    processes = client.get_folder_by_id(PRE_FOLDER_ID).get_processes()
    for p in processes:
        process_atr = p.__dict__
        assert process_atr["client_id"]
        assert process_atr["refresh_token"]
        assert process_atr["folder_id"]
        assert process_atr["tenant_name"]
        assert process_atr["id"]
        assert process_atr["access_token"]
        assert process_atr["version"]
        assert process_atr["title"]
        assert process_atr["key"]


def test_folder_process_keys():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    process_ids = client.get_folder_by_id(PRE_FOLDER_ID).get_processes_keys()
    pprint(process_ids)
    assert process_ids


def test_folder_processes_by_key():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    process = client.get_folder_by_id(PRE_FOLDER_ID).get_process_by_key("BOT_048_FR_PQ_AnaelIntegration:1.0.2-alpha.59")
    process_atr = process.__dict__
    assert process_atr["client_id"]
    assert process_atr["refresh_token"]
    assert process_atr["folder_id"]
    assert process_atr["tenant_name"]
    assert process_atr["id"]
    assert process_atr["access_token"]
    assert process_atr["version"]
    assert process_atr["title"]
    assert process_atr["key"]
    print(process)


def test_folder_queues():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    queues = client.get_folder_by_id(PRE_FOLDER_ID).get_queues()
    for q in queues:
        queue_atr = q.__dict__
        assert queue_atr["client_id"]
        assert queue_atr["refresh_token"]
        assert queue_atr["folder_id"]
        assert queue_atr["id"]
        assert queue_atr["name"]
        assert queue_atr["tenant_name"]
        assert queue_atr["access_token"]


def test_folder_info():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN2, tenant_name=TENANT_NAME)
    info = client.get_folder_by_id(PROD_FOLDER_ID).info()
    assert info["DisplayName"]
    assert info["FeedType"]
    assert info["FullyQualifiedName"]
    assert info["FullyQualifiedNameOrderable"]
    assert info["Id"]
    assert info["IsActive"]
    assert info["Key"]
    assert info["PermissionModel"]
    assert info["ProvisionType"]


test_folder_info()


def test_folder_queue_ids():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    queue_ids = client.get_folder_by_id(PRE_FOLDER_ID).get_queue_ids()
    assert queue_ids


def test_folder_processing_records():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    processing_records = client.get_folder_by_id(PRE_FOLDER_ID).get_processing_records()
    for r in processing_records:
        assert r["Id"]
        assert r["QueueDefinitionId"]
        assert r["QueueDefinitionName"]


def test_folder_queue_by_id():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    queue = client.get_folder_by_id(PRE_FOLDER_ID).get_queue_by_id(QUEUE_ID)
    queue_atr = queue.__dict__
    assert queue_atr["client_id"]
    assert queue_atr["refresh_token"]
    assert queue_atr["tenant_name"]
    assert queue_atr["id"]
    assert queue_atr["session"]
    assert queue_atr["folder_name"]
    assert queue_atr["folder_id"]
    assert queue_atr["folder_name"]
    print(queue)


def test_folder_assets():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    assets = client.get_folder_by_id(PRE_FOLDER_ID).get_assets()
    for asset in assets:
        asset_atr = asset.__dict__
        assert asset_atr["client_id"]
        assert asset_atr["refresh_token"]
        assert asset_atr["access_token"]
        assert asset_atr["tenant_name"]
        assert asset_atr["id"]
        assert asset_atr["session"]
        assert asset_atr["name"]
        assert asset_atr["folder_id"] == int(PRE_FOLDER_ID)


def test_folder_asset_ids():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    asset_ids = client.get_folder_by_id(PRE_FOLDER_ID).get_asset_ids()
    assert asset_ids
    pprint(asset_ids)


def test_folder_asset_by_id():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    asset = client.get_folder_by_id(PRE_FOLDER_ID).get_asset_by_id("261170")
    asset_atr = asset.__dict__
    assert asset_atr["client_id"]
    assert asset_atr["refresh_token"]
    assert asset_atr["access_token"]
    assert asset_atr["tenant_name"]
    assert asset_atr["id"]
    assert asset_atr["session"]
    assert asset_atr["name"]
    assert asset_atr["folder_id"] == int(PRE_FOLDER_ID)


def test_folder_process_schedules():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    proc_schedules = client.get_folder_by_id(PROD_FOLDER_ID).get_process_schedules()
    for schedule in proc_schedules:
        schedule_atr = schedule.__dict__
        assert schedule_atr["client_id"]
        assert schedule_atr["refresh_token"]
        assert schedule_atr["access_token"]
        assert schedule_atr["tenant_name"]
        assert schedule_atr["id"]
        assert schedule_atr["session"]
        assert schedule_atr["name"]
        assert schedule_atr["folder_id"] == int(PROD_FOLDER_ID)


def test_folder_schedule_ids():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    schedule_ids = client.get_folder_by_id(PROD_FOLDER_ID).get_schedule_ids()
    assert schedule_ids


def test_folder_process_schedule_by_id():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    proc_schedule = client.get_folder_by_id(PROD_FOLDER_ID).get_schedule_by_id(70790)
    assert proc_schedule.client_id
    assert proc_schedule.tenant_name
    assert proc_schedule.id == 70790
    assert proc_schedule.name
    assert proc_schedule.folder_id == int(PROD_FOLDER_ID)
    print(proc_schedule)


def test_folder_jobs():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    jobs = client.get_folder_by_id(PRE_FOLDER_ID).get_jobs()
    for job in jobs:
        job_atr = job.__dict__
        assert job_atr["client_id"]
        assert job_atr["refresh_token"]
        assert job_atr["access_token"]
        assert job_atr["tenant_name"]
        assert job_atr["id"]
        assert job_atr["key"]
        assert job_atr["folder_name"]
        assert job_atr["session"]
        assert job_atr["folder_id"] == int(PRE_FOLDER_ID)


def test_folder_job_by_key():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    job = client.get_folder_by_id(PRE_FOLDER_ID).get_job_by_key("507491b2-8ec3-48d8-b651-cd2a225f51dd")
    job_atr = job.__dict__
    assert job_atr["client_id"]
    assert job_atr["tenant_name"]
    assert job_atr["access_token"]
    assert job_atr["folder_id"]
    assert job_atr["folder_name"]
    assert job_atr["id"]
    assert job_atr["key"]
    print(job)

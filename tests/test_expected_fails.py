from orchestrator.orchestrator import Orchestrator
from orchestrator.orchestrator_asset import Asset
from orchestrator.orchestrator_folder import Folder
from orchestrator.orchestrator_job import Job
from orchestrator.orchestrator_library import Library
from orchestrator.orchestrator_logs import Log
from orchestrator.orchestrator_machine import Machine
from orchestrator.orchestrator_process import Process
from orchestrator.orchestrator_process_schedule import ProcessSchedule
from orchestrator.orchestrator_queue import Queue
from orchestrator.orchestrator_queue_item import QueueItem
from orchestrator.exceptions import OrchestratorAuthException, OrchestratorFormatException, OrchestratorMissingParam
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


@pytest.mark.xfail(raises=OrchestratorAuthException)
def test_orchestrator_init_xfails():
    Orchestrator(refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    Orchestrator(client_id=CLIENT_ID, tenant_name=TENANT_NAME)
    Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN)


@pytest.mark.xfail(raises=OrchestratorAuthException)
def test_orchestrato_folder_xfail():
    client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    client._folder_header()


@pytest.mark.xfail(raises=OrchestratorMissingParam)
def test_xfail_asset_init():
    Asset(
        client_id="1234",
        refresh_token="1234",
        tenant_name="1234",
        folder_id=1234534,
        folder_name="Some name",
        session=None,
        asset_name="Some other name",
        access_token="12313"
    )


@pytest.mark.xfail(raises=OrchestratorMissingParam)
def test_xfail_folder_init():
    Folder(
        client_id="1234",
        refresh_token="1234",
        tenant_name="1234",
        folder_name="Some name",
        session=None,
        access_token="12313"
    )


@pytest.mark.xfail(raises=OrchestratorMissingParam)
def test_xfail_folder_init():
    Folder(
        client_id="1234",
        refresh_token="1234",
        tenant_name="1234",
        folder_name="Some name",
        session=None,
        access_token="12313"
    )


@pytest.mark.xfail(raises=OrchestratorMissingParam)
def test_xfail_job_init():
    Job(
        client_id="1234",
        refresh_token="1234",
        tenant_name="1234",
        folder_id=123343,
        folder_name="Some name",
        session=None,
        job_id="dasdjkl1234",
        access_token="12313"
    )


@pytest.mark.xfail(raises=OrchestratorMissingParam)
def test_xfail_library_init():
    Library(
        client_id="1234",
        refresh_token="1234",
        tenant_name="1234",
        session=None,
        lib_id="dasdjkl1234",
        access_token="12313"
    )


@pytest.mark.xfail(raises=OrchestratorMissingParam)
def test_xfail_log_init():
    Log(
        client_id="1234",
        refresh_token="1234",
        tenant_name="1234",
        folder_id=123343,
        folder_name="Some name",
        session=None,
    )


@pytest.mark.xfail(raises=OrchestratorMissingParam)
def test_xfail_machine_init():
    Machine(
        client_id="1234",
        refresh_token="1234",
        tenant_name="1234",
        folder_id=123343,
        session=None,
        access_token="12313"
    )


@pytest.mark.xfail(raises=OrchestratorMissingParam)
def test_xfail_process_schedule_init():
    ProcessSchedule(
        client_id="1234",
        refresh_token="1234",
        tenant_name="1234",
        folder_id=123343,
        session=None,
        access_token="12313"
    )


@pytest.mark.xfail(raises=OrchestratorMissingParam)
def test_xfail_process_init():
    Process(
        client_id="1234",
        refresh_token="1234",
        tenant_name="1234",
        folder_id=123343,
        session=None,
        access_token="12313"
    )


@pytest.mark.xfail(raises=OrchestratorMissingParam)
def test_xfail_queue_item_init():
    QueueItem(
        client_id="1234",
        refresh_token="1234",
        tenant_name="1234",
        folder_id=123343,
        session=None,
        access_token="12313"
    )


@pytest.mark.xfail(raises=OrchestratorMissingParam)
def test_xfail_queue_init():
    Queue(
        client_id="1234",
        refresh_token="1234",
        tenant_name="1234",
        folder_id=123343,
        session=None,
        access_token="12313"
    )

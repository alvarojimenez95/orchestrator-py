from orchestrator.orchestrator import Orchestrator
from dotenv import load_dotenv
import os
from pprint import pprint
import pytest

LOCAL_TEST = True

if LOCAL_TEST:
    load_dotenv()
    DUMMY_TOKEN = os.getenv('DUMMY_TOKEN')
    CLIENT_ID = os.getenv('CLIENT_ID')
    REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
    REFRESH_TOKEN_BOTS_OPS = os.getenv('REFRESH_TOKEN_BOTS_OPS')

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


def test_orchestrator_wrong_parameters():
    client = Orchestrator(client_id=CLIENT_ID,
                          refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    folder = client.get_folder_by_id(PRE_FOLDER_ID)
    data = {
        "$filter": "Name eq 'BOT_048_FR_AnaelIntegration'"
    }
    queue = folder.get_queues(options=data)
    print(queue)
    # queue = folder.get_queue_by_id


test_orchestrator_wrong_parameters()


def test_orchestrator_folder():
    client = Orchestrator(client_id=CLIENT_ID,
                          refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    folder = client.get_folder_by_id(PRE_FOLDER_ID)
    folder_atr = folder.__dict__
    assert folder_atr["client_id"]
    assert folder_atr["refresh_token"]
    assert folder_atr["folder_id"]
    assert folder_atr["tenant_name"]
    assert folder_atr["id"]
    assert folder_atr["access_token"]


def test_orchestrator_folders():
    client = Orchestrator(client_id=CLIENT_ID,
                          refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    folders = client.get_folders()
    for folder in folders:
        folder_atr = folder.__dict__
        assert folder_atr["client_id"]
        assert folder_atr["refresh_token"]
        assert folder_atr["folder_id"]
        assert folder_atr["tenant_name"]
        assert folder_atr["id"]
        assert folder_atr["access_token"]


def test_orchestrator_folder_ids():
    client = Orchestrator(client_id=CLIENT_ID,
                          refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    folder_ids = client.get_folder_ids()
    assert folder_ids


def test_orchestrator_folder_by_name():
    client = Orchestrator(client_id=CLIENT_ID,
                          refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    folder = client.get_folder_by_name("Pre-produccion")
    folder_atr = folder.__dict__
    assert folder_atr["client_id"]
    assert folder_atr["refresh_token"]
    assert folder_atr["folder_id"]
    assert folder_atr["tenant_name"]
    assert folder_atr["id"]
    assert folder_atr["access_token"]


@pytest.mark.xfail(raises=Exception)
def test_xfail_folder_name():
    client = Orchestrator(client_id=CLIENT_ID,
                          refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    client.get_folder_by_name("Pre-production")


def test_libreries():
    client = Orchestrator(client_id=CLIENT_ID,
                          refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    libraries = client.get_libraries()
    for lib in libraries:
        lib_atr = lib.__dict__
        assert lib_atr["client_id"]
        assert lib_atr["access_token"]
        assert lib_atr["tenant_name"]
        assert lib_atr["id"]
        assert lib_atr["key"]
        assert lib_atr["name"]
        assert lib_atr["session"]
        print(lib)


def test_machines():
    client = Orchestrator(client_id=CLIENT_ID,
                          refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    machines = client.get_machines()
    for m in machines:
        machine_atr = m.__dict__
        assert machine_atr["client_id"]
        assert machine_atr["tenant_name"]
        assert machine_atr["id"]
        assert machine_atr["key"]
        assert machine_atr["name"]
        print(machine_atr["name"])
        assert machine_atr["session"]


def test_machine_ids():
    client = Orchestrator(client_id=CLIENT_ID,
                          refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    machine_ids = client.get_machine_ids()


def test_machine_by_id():
    client = Orchestrator(client_id=CLIENT_ID,
                          refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    machine = client.get_machine_by_id(123680)
    machine_atr = machine.__dict__
    assert machine_atr["id"]
    assert machine_atr["name"]
    assert machine_atr["key"]
    assert machine_atr["tenant_name"]
    print(machine)


def test_permissions():
    client = Orchestrator(client_id=CLIENT_ID,
                          refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)
    client.permissions()


def test_orchestrator_auth_from_file():
    client = Orchestrator(
        file="/Users/alvaro/Dev/python/orchestrator-py/tests/dummy_creds.json")


# test_orchestrator_auth_from_file()

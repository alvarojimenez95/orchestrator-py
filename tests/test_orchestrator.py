from orchestrator.orchestrator import Orchestrator


def test_init():
    Orchestrator(client_id='123', refresh_token='123', tenant_name='test')
    pass

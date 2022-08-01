from orchestrator.orchestrator_http import OrchestratorHTTP
import requests
from orchestrator.exceptions import OrchestratorMissingParameters


class Library(OrchestratorHTTP):
    def __init__(self, client_id, refresh_token, tenant_name, session=None, lib_key=None, lib_id=None, lib_title=None, folder_id=None, access_token=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, tenant_name=tenant_name, folder_id=folder_id, session=session)
        if not lib_key or not lib_id:
            raise OrchestratorMissingParameters(error_message="Required parameter(s) missing: library key",
                                                message="Required parameter(s) missing: library key")
        self.client_id = client_id
        self.tenant_name = tenant_name
        self.access_token = access_token
        self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
        self.folder_id = folder_id
        self.id = lib_id
        self.key = lib_key
        self.name = lib_title
        if session:
            self.session = session
        else:
            self.session = requests.Session()

    def __str__(self):
        idx = f"Id: {self.id}\n"
        key = f"Key: {self.key}\n"
        title = f"Title: {self.name}\n"

        return f"{idx}{key}{title}"

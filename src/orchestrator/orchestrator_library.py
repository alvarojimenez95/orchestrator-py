from orchestrator.orchestrator_http import OrchestratorHTTP
import requests
from orchestrator.exceptions import OrchestratorMissingParam


class Library(OrchestratorHTTP):
    def __init__(self, client_id, refresh_token, tenant_name, session=None, lib_key=None, lib_id=None, lib_title=None, folder_id=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, tenant_name=tenant_name, folder_id=folder_id, session=session)
        if not lib_key:
            raise OrchestratorMissingParam(value="library key",
                                           message="Required parameter(s) missing: library key")
        self.tenant_name = tenant_name
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

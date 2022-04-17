from orchestrator.orchestrator_http import OrchestratorHTTP
import requests
from orchestrator.exceptions import OrchestratorMissingParam


class Asset(OrchestratorHTTP):
    def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, folder_name=None, session=None, asset_id=None, asset_name=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, tenant_name=tenant_name, folder_id=folder_id, session=session)
        if not asset_id:
            raise OrchestratorMissingParam(value="asset_id",
                                           message="Required parameter(s) missing: asset_id")
        self.tenant_name = tenant_name
        self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
        self.folder_id = folder_id
        self.folder_name = folder_name
        self.id = asset_id
        self.name = asset_name
        if session:
            self.session = session
        else:
            self.session = requests.Session()

    def info(self):
        endpoint = f"/Assets({self.id})"
        url = f"{self.base_url}{endpoint}"
        return self._get(url)

    def edit(self, body=None):
        endpoint = f"/Assets({self.id})"
        url = f"{self.base_url}{endpoint}"
        return self._put(url, body=body)

    def delete(self, body=None):
        endpoint = f"/Assets({self.id})"
        url = f"{self.base_url}{endpoint}"
        return self._delete(url, body=body)

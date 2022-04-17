from orchestrator.orchestrator_http import OrchestratorHTTP
from orchestrator.exceptions import OrchestratorMissingParam
import requests

__all__ = ["ProcessSchedule"]


class ProcessSchedule(OrchestratorHTTP):
    def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, session=None, process_id=None, process_name=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, tenant_name=tenant_name, folder_id=folder_id)
        if not tenant_name or not folder_id:
            raise OrchestratorMissingParam(value="tenant_name, folder_id",
                                           message="Required parameter(s) missing: tenant_name, folder_id")
        self.tenant_name = tenant_name
        self.id = process_id
        self.name = process_name
        self.folder_id = folder_id
        self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
        if session:
            self.session = session
        else:
            self.session = requests.Session()

    def __str__(self):

        return f"Schedule Id: {self.id} \nName: {self.name}"

    def info(self):
        endpoint = f"/ProcessSchedules({self.id})"
        url = f"{self.base_url}{endpoint}"
        return self._get(url)

    def schedule(self):
        info = self.info()
        return info["StartProcessCronSummary"]

    def delete(self):
        """
            Deletes a schedule
        """
        endpoint = f"/ProcessSchedules({self.id})"
        url = f"{self.base_url}{endpoint}"
        return self._delete(url)

    def enable(self, enable: bool = False, schedule_ids=[]):
        schedule_ids.append(self.id)
        endpoint = "/ProcessSchedules"
        uipath_svc = "/UiPath.Server.Configuration.OData.SetEnabled"
        body = {
            "enabled": enable,
            "scheduleIds": schedule_ids
        }
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        return self._post(url, body=body)

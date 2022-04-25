from orchestrator.orchestrator_http import OrchestratorHTTP
import requests
from orchestrator.exceptions import OrchestratorMissingParam


class Job(OrchestratorHTTP):
    def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, folder_name=None, session=None, job_id=None, job_key=None, job_name=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, tenant_name=tenant_name, folder_id=folder_id, session=session)
        if not job_key:
            raise OrchestratorMissingParam(value="asset_id",
                                           message="Required parameter(s) missing: asset_id")
        self.tenant_name = tenant_name
        self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
        self.folder_id = folder_id
        self.folder_name = folder_name
        self.id = job_id
        self.key = job_key
        self.name = job_name
        if session:
            self.session = session
        else:
            self.session = requests.Session()

    def __str__(self):
        print(f"Key: {self.id}")
        print(f"Name: {self.name}")

    def info(self):
        endpoint = f"/Jobs({self.id})"
        url = f"{self.base_url}{endpoint}"
        return self._get(url)

    def stop(self):
        """
        Stops the given job
        """
        endpoint = f"/Jobs({self.id})"
        uipath_svc = "/UiPath.Server.Configuration.OData.StopJob"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        cancel_body = {
            "strategy": "SoftStop"
        }
        return self._post(url, body=cancel_body)

    def kill(self):
        """
        Kill the given job
        """
        endpoint = f"/Jobs({self.id})"
        uipath_svc = "/UiPath.Server.Configuration.OData.StopJob"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        cancel_body = {
            "strategy": "Kill"
        }
        return self._post(url, body=cancel_body)

    def restart(self):
        """
        Restarts the given job
        """
        endpoint = f"/Jobs"
        uipath_svc = "/UiPath.Server.Configuration.OData.RestartJob"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        restart_body = {
            "jobId": self.id
        }
        return self._post(url, body=restart_body)

    def resume(self):
        """
        Restarts the given job
        """
        endpoint = f"/Jobs"
        uipath_svc = "/UiPath.Server.Configuration.OData.ResumeJob"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        resume_body = {
            "jobKey": self.key
        }
        return self._post(url, body=resume_body)

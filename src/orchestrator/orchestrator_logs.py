from datetime import datetime
from orchestrator.orchestrator_http import OrchestratorHTTP
import requests
from orchestrator.exceptions import OrchestratorMissingParam


class Log(OrchestratorHTTP):
    def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, folder_name=None, session=None, msg=None, trace=None, key=None, stamp=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, tenant_name=tenant_name, folder_id=folder_id, session=session)
        if not key:
            raise OrchestratorMissingParam(value="job key",
                                           message="Required parameter(s) missing: key")
        self.tenant_name = tenant_name
        self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
        self.folder_id = folder_id
        self.folder_name = folder_name
        self.key = key
        self.message = msg
        self.timestamp = stamp
        self.trace = trace
        if session:
            self.session = session
        else:
            self.session = requests.Session()

    def __str__(self):
        return f"Job Key: {self.key}\nMessage: {self.message}\nTimeStamp: {self.timestamp}\nTrace: {self.trace}"

    def create(self, level="Info", message=None):
        endpoint = "/api/Logs/SubmitLogs"
        body = {
            "message": message,
            "level": level,
            "timeStamp": datetime.now,
            "jobId": self.id
        }
        url = f"{self.base_url}{endpoint}"
        return self._post(url, body=body)

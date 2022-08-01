from platform import machine
from orchestrator.exceptions import OrchestratorMissingParameters
from orchestrator.orchestrator_http import OrchestratorHTTP
import requests
from urllib.parse import urlencode


class Machine(OrchestratorHTTP):
    """
    Constructor. 

    @client_id: the client id 
    @refresh_token: a refresh token  
    @tenant_name: account's logical name
    @folder_id: the folder id 
    @folder_name: the folder name
    @session: a session object (options)
    @queue_name: the queue name
    @queue_id: the queue id
    """

    def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, session=None, machine_id=None, machine_key=None, machine_name=None, access_token=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, tenant_name=tenant_name, folder_id=folder_id, session=session)
        if not machine_id:
            raise OrchestratorMissingParameters(
                message="Required parameter(s) missing: machine_id",
                error_message="Required parameter(s) missing: machine_id"

            )
        self.id = machine_id
        self.access_token = access_token
        self.name = machine_name
        self.key = machine_key
        self.folder_id = folder_id
        self.tenant_name = tenant_name
        self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
        if session:
            self.session = session
        else:
            self.session = requests.Session()

    def __str__(self):
        return f"Machine Id: {self.id} \nMachine Name: {self.name}"

    def info(self):
        endpoint = f"/Machines({self.id})"
        url = f"{self.base_url}{endpoint}"
        return self._get(url)

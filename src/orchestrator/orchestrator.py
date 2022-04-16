from http import client
from orchestrator.orchestrator_http import OrchestratorHTTP
import requests
from urllib.parse import urlencode
from orchestrator.orchestrator_folder import Folder
from orchestrator.orchestrator_process import Process


class Orchestrator(OrchestratorHTTP):
    def __init__(
        self,
        client_id,
        refresh_token,
        tenant_name,
        folder_id=None,
        session=None

    ):
        super().__init__(client_id=client_id, refresh_token=refresh_token, tenant_name=tenant_name, folder_id=folder_id, session=session)
        # if not client_id or not refresh_token:
        #     raise OrchestratorAuthException(
        #         value=None, message="client id and refresh token cannot be left empty"
        #     )
        # else:
        #     self.client_id = client_id
        self.client_id = client_id
        self.refresh_token = refresh_token
        self.folder_id = folder_id
        self.tenant_name = tenant_name
        self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
        if session:
            print("session set")
            self.session = session
        else:
            print("session not set")
            self.session = requests.Session()

    def __str__(self):
        return f"Folder Id: {self.folder_id} \nTenant: {self.tenant_name}"

    def get_all_folders(self, options=None):
        """
            Gets all the folders from a given Organization Unit
        """
        endpoint = "/Folders"
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}"
        data = self._get(url)
        filt_data = data['value']
        return [Folder(self.client_id, self.refresh_token, self.tenant_name, self.session, folder["DisplayName"], folder["Id"]) for folder in filt_data]

    def get_folder_ids(self, options=None):
        """
            Returns a python list of dictionaries
            with all the folder names as keys
            and the folder ids as values
        """
        folders = self.get_all_folders(options)
        ids = {}
        for folder in folders:
            ids.update({folder.id: folder.name})
        return ids

    def get_folder_by_id(self, folder_id):
        ids = self.get_folder_ids()
        self.folder_id = folder_id
        folder_name = ids[folder_id]
        return Folder(client_id=self.client_id, refresh_token=self.refresh_token, tenant_name=self.tenant_name,  session=self.session, folder_name=folder_name, folder_id=folder_id)

    def get_folder_by_name(self, folder_name):
        pass

    def usernames(self, options=None):
        """
            No se por que no va
        """
        endpoint = "/Sessions"
        uipath_svc = "/UiPath.Server,Configuration.OData.GetUsernames"
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}{uipath_svc}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}{uipath_svc}"
        return self._get(url)

    def get_all_processes(self, options=None):
        endpoint = "/Processes"
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}"
        processes = self._get(url)["value"]
        return [Process(self.client_id, self.refresh_token, self.tenant_name, self.folder_id, self.session, process["Id"], process["Title"], process["Version"], process["Key"]) for process in processes]

    def get_processes_keys(self, options=None):
        """
            Returns a dictionary
                process title -- process key
        """
        processes = self.get_all_processes(options=options)
        ids = {}
        for process in processes:
            ids.update({process.key: process.title})
        return ids

    def get_process_by_key(self, process_key):
        query_param = urlencode({
            "$filter": f"Key eq '{process_key}"
        })
        endpoint = "/Processes"
        url = f"{self.base_url}{endpoint}?{query_param}"
        process = self._get(url)["value"][0]
        return Process(self.client_id, self.refresh_token, self.tenant_name, self.folder_id,
                       self.session, process["Id"], process["Title"], process["Version"], process["Key"])


from typing import List
from orchestrator.orchestrator_http import OrchestratorHTTP
import requests
import json
from urllib.parse import urlencode
from orchestrator.orchestrator_folder import Folder
from orchestrator.orchestrator_library import Library
from orchestrator.orchestrator_process import Process


__all__ = ["Orchestrator"]

"""
Parent class for initializing a client for UiPath's Orchestrator's API
"""


class Orchestrator(OrchestratorHTTP):
    """
    Constructor. 

    @client_id: the client id 
    @refresh_token: a refresh token  
    @tenant_name: account's logical name
    @folder_id: a folder id (optional)
    @session: a session object (options)
    @file: a credentials file containing client_id, refresh_token and tenant_name (optional) 
    """

    def __init__(
        self,
        client_id=None,
        refresh_token=None,
        tenant_name=None,
        folder_id=None,
        session=None,
        file=None

    ):

        super().__init__(client_id=client_id, refresh_token=refresh_token, tenant_name=tenant_name, folder_id=folder_id, session=session, file=file)
        # if not client_id or not refresh_token:
        #     raise OrchestratorAuthException(
        #         value=None, message="client id and refresh token cannot be left empty"
        #     )
        # else:
        #     self.client_id = client_id
        if file:
            self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"

            try:
                f = open(file)
                data = json.load(f)
                self.client_id = data["client_id"]
                self.refresh_token = data["refresh_token"]
                self.tenant_name = data["tenant_name"]
            except KeyError:
                raise
        else:
            self.client_id = client_id
            self.refresh_token = refresh_token
            self.tenant_name = tenant_name
            self.folder_id = folder_id
            self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
        if session:
            print("session set")
            self.session = session
        else:
            print("session not set")
            self.session = requests.Session()

    def __str__(self):
        if self.folder_id:
            return f"Folder Id: {self.folder_id} \nTenant: {self.tenant_name}"
        return {f"Tenant: {self.tenant_name}"}

    def get_folders(self, options=None):
        """
        Gets all the folders from a given organization

        @options: dictionary of odata filtering options
        ========
        @returns: a list of Folders of the given organization
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
            Returns a dictionary with the folder ids 

            @options: dictionary of odata filtering options
            =======
            @returns: a dictionary where the keys are the ids 
            and the values the names of the folders in the given
            organization 
        """
        folders = self.get_folders(options)
        ids = {}
        for folder in folders:
            ids.update({folder.id: folder.name})
        return ids

    def get_folder_by_id(self, folder_id):
        """
        Returns a single folder by its id 

        @folder_id: the id of the folder
        ==========
        @returns: a Folder object with the specified folder id
        """
        ids = self.get_folder_ids()
        self.folder_id = folder_id
        folder_name = ids[folder_id]
        return Folder(client_id=self.client_id, refresh_token=self.refresh_token, tenant_name=self.tenant_name,  session=self.session, folder_name=folder_name, folder_id=folder_id)

    def get_folder_by_name(self, folder_name):
        """
            Returns a single folder by its name

            @folder_name: the name of the folder
            ============
            @returns: a Folder object with the specified folder_name
        """
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

    def get_processes(self, options=None):
        """
        Gets all the processes of a given organization

        @options: a dictionary of odata filtering options
        ========
        @returns: a list of Processes of the given organization
        """
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
            Returns a dictionary with the processes keys

            @options: dictionary of odata filtering options
            ========
            @returns: a dictionary where the keys are the process'
            key and the values the process' title of the processes 
            in the given organization
        """
        processes = self.get_processes(options=options)
        ids = {}
        for process in processes:
            ids.update({process.key: process.title})
        return ids

    def get_process_by_key(self, process_key):
        """
        Returns a single process by is key

        @process_key: the key of the process 
        ============
        @returns: a Process object with the specified process key 
        """
        query_param = urlencode({
            "$filter": f"Key eq '{process_key}"
        })
        endpoint = "/Processes"
        url = f"{self.base_url}{endpoint}?{query_param}"
        process = self._get(url)["value"][0]
        return Process(self.client_id, self.refresh_token, self.tenant_name, self.folder_id,
                       self.session, process["Id"], process["Title"], process["Version"], process["Key"])

    def get_libraries(self, options=None):
        """
        Gets all the libraries of a given organization

        @options: a dictionary of odata filtering options
        ========
        @returns: a list of Libraries of the given organization
        """
        endpoint = "/Libraries"
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}"
        libraries = self._get(url)["value"]
        return [Library(self.client_id, self.refresh_token, self.tenant_name, self.session,  lib["Key"], lib["Id"], lib["Title"], self.folder_id) for lib in libraries]

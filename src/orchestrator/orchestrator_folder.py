from orchestrator.orchestrator_http import OrchestratorHTTP
from orchestrator.orchestrator_asset import Asset
from orchestrator.orchestrator_queue import Queue
from orchestrator.orchestrator_job import Job
from orchestrator.orchestrator_process_schedule import ProcessSchedule
from orchestrator.exceptions import OrchestratorMissingParam
from urllib.parse import urlencode
import requests


"""
Class to deal with calls and requests from a given Folder of an Orchestrator Cloud instance

"""


class Folder(OrchestratorHTTP):
    """Constructor 

    :param client_id - the client id of your organization 
    :type client_id - str 

    :param refresh_token - a refresh token. 
    :type refresh_token - str 

    :param tenant_name - your account's logical name
    :type tenant_name - str 

    :param session - an optional session object 
    :type session - Session

    :param folder_id - the id of the folder (UiPath's organizations unit)
    :type folder_id - str 

    :param folder_name - the name of the folder 
    :type folder_name : str
    """

    def __init__(self, client_id, refresh_token, tenant_name, session=None, folder_name=None,  folder_id=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, tenant_name=tenant_name, folder_id=folder_id, session=session)
        if not tenant_name or not folder_id:
            raise OrchestratorMissingParam(value="tenant_name",
                                           message="Required parameter missing: tenant_name")
        self.id = folder_id
        self.tenant_name = tenant_name
        self.name = folder_name
        self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
        if session:
            self.session = session
        else:
            self.session = requests.Session()

    def __str__(self):
        return f"Folder Id: {self.id} \nFolder Name: {self.name}"

    def info(self):
        """Returns a information of a single
            folder based on its folder id
        """
        endpoint = f"/Folders({self.id})"
        url = f"{self.base_url}{endpoint}"
        data = self._get(url)
        return data

    def get_queues(self, options=None):
        """Parameters:
            :param options - dictionary of filtering odata options
            :type options - dict
        """
        endpoint = "/QueueDefinitions"
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}"
        data = self._get(url)
        filt_data = data['value']
        return [Queue(self.client_id, self.refresh_token, self.tenant_name, self.id, self.name, self.session, queue["Name"],  queue["Id"]) for queue in filt_data]

    def get_queue_ids(self, options=None):
        """
            Returns a list of dictionaries containing
            the queue name and the queue id

            :options dictionary for odata options

        """
        queues = self.get_queues(options)
        ids = {}
        for queue in queues:
            ids.update({queue.id: queue.name})
        return ids

    def get_processing_records(self, options=None):
        """Returns a list of queue processing records for all the queues

            :param options - dictionary for odata options
            :type options - dict


        """
        endpoint = "/QueueProcessingRecords"
        uipath_svc = "/UiPathODataSvc.RetrieveQueuesProcessingStatus"
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}{uipath_svc}"
        data = self._get(url)
        return data['value']

    def get_queue_by_id(self, queue_id):
        queues = self.get_queue_ids()
        return Queue(self.client_id, self.refresh_token, self.tenant_name, self.id, self.name, self.session, queues[queue_id], queue_id=queue_id)

    def get_assets(self, options=None):
        """
            Returns list of assets
            :options dict of odata filter options
        """
        endpoint = "/Assets"
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}"
        data = self._get(url)
        # pprint(data)
        # pprint(self.id)
        filt_data = data['value']
        return [Asset(self.client_id, self.refresh_token, self.tenant_name, self.id, self.name, self.session, asset["Id"], asset["Name"]) for asset in filt_data]

    def get_asset_ids(self, options=None):
        """
            Returns a dictionary of ky value pairs
            where keys are the assets names and the values
            are the ids


            :param options - dictionary of odata filter options
        """

        assets = self.get_assets(options)
        ids = {}
        for asset in assets:
            ids.update({asset.id: asset.name})
        return ids

    def get_asset_by_id(self, asset_id):
        assets = self.get_asset_ids()
        return Asset(self.client_id, self.refresh_token, self.tenant_name, self.id, self.name, self.session, asset_id, assets[asset_id])

    def create_asset(self, body=None):
        pass

    def get_process_schedules(self, options=None):
        endpoint = "/ProcessSchedules"
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}"
        data = self._get(url)
        filt_data = data["value"]
        return [ProcessSchedule(self.client_id, self.refresh_token, self.tenant_name, self.folder_id, self.session, process["Id"], process["Name"]) for process in filt_data]

    def get_schedule_ids(self, options=None):
        """
            Returns a list of dictionaries
                name -- schedule_id
        """
        process_schedules = self.get_process_schedules(options=options)
        ids = {}
        for schedule in process_schedules:
            ids.update({schedule.id: schedule.name})
        return ids

    def get_sessions(self, options=None):
        """
            Gets all the sessions for the current folder
        """
        endpoint = "/Sessions"
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}"
        return self._get(url)["value"]

    def get_machine_runtime_sessions(self):
        """
            No se por que no va
        """
        endpoint = "/Sessions"
        uipath_svc = "UiPath.Server.Configuration.OData.GetMachineSessionRuntimesByFolderId(folderId={self.id})"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        return self._get(url)

    def get_jobs(self, options=None):
        """
        Returns the jobs of a given folder
        """
        endpoint = "/Jobs"
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}"
        data = self._get(url)["value"]
        return [Job(self.client_id, self.refresh_token, self.tenant_name, self.id, self.name, self.session, job["Id"], job["Key"], job["ReleaseName"]) for job in data]

    def job_triggers(self, options=None):
        endpoint = "/JobTriggers"
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}"
        return self._get(url)["value"]

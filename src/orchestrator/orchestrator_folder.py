from orchestrator.orchestrator_http import OrchestratorHTTP
from orchestrator.orchestrator_asset import Asset
from orchestrator.orchestrator_queue import Queue
from orchestrator.orchestrator_job import Job
from orchestrator.orchestrator_process import Process
from orchestrator.orchestrator_process_schedule import ProcessSchedule
from orchestrator.exceptions import (
    OrchestratorMissingParameters,
    OrchestratorQueueNotFound,
    OrchestratorAssetNotFound,
    OrchestratorJobNotFound,
    OrchestratorProcessNotFound,
    OrchestratorProcessScheduleNotFound)
from urllib.parse import urlencode
import requests
from pprint import pprint

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

    def __init__(self, client_id, refresh_token, tenant_name, session=None, folder_name=None,  folder_id=None, access_token=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token,
                         tenant_name=tenant_name, folder_id=folder_id, session=session)
        if not tenant_name or not folder_id:
            raise OrchestratorMissingParameters(
                message="Required parameter missing: tenant_name",
                error_message="Required parameter missing: tenant_name")
        self.id = folder_id
        self.access_token = access_token
        self.refresh_token = refresh_token
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
        return [Queue(self.client_id, self.access_token, self.tenant_name, self.id, self.name, self.session, queue["Name"],  queue["Id"], access_token=self.access_token) for queue in filt_data]

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
        """Returns a single queue by its id"""
        queues = self.get_queue_ids()
        try:
            return Queue(self.client_id, self.refresh_token, self.tenant_name, self.id, self.name, self.session, queues[int(queue_id)], queue_id=int(queue_id), access_token=self.access_token)
        except KeyError:
            raise OrchestratorQueueNotFound(message=f"Queue {queue_id} not found",
                                            error_message=f"Queue {queue_id} does not appear to exist in the current folder.")

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
        filt_data = data['value']
        return [Asset(self.client_id, self.refresh_token, self.tenant_name, self.id, self.name, self.session, asset["Id"], asset["Name"], access_token=self.access_token) for asset in filt_data]

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
        """
            Gets a single asset by its id 

            Parameters: 

            :param asset_id - the id of the asset
        """
        assets = self.get_asset_ids()
        try:
            return Asset(self.client_id, self.refresh_token, self.tenant_name, self.id, self.name, self.session, int(asset_id), assets[int(asset_id)], access_token=self.access_token)
        except KeyError:
            raise OrchestratorAssetNotFound(message=f"Queue {asset_id} not found",
                                            error_message=f"Queue {asset_id} does not appear to exist in the current folder.")

    def create_asset(self, body=None):
        pass

    def get_process_schedules(self, options=None):
        """
            Returns a list of the process schedules in the current 
            folder 

            Parameters: 
            :param options - a dictionary of odata query parameters
        """
        endpoint = "/ProcessSchedules"
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}"
        data = self._get(url)
        filt_data = data["value"]
        return [ProcessSchedule(self.client_id, self.refresh_token, self.tenant_name, self.folder_id, self.session, process["Id"], process["Name"], access_token=self.access_token) for process in filt_data]

    def get_schedule_by_id(self, id):
        """
            Returns a single process schedule by its id 

            Parameters:

            :param id - the id of the process schedule
        """
        query_filter = urlencode({"$filter": f"Id eq {id}"})

        endpoint = "/ProcessSchedules"
        url = f"{self.base_url}{endpoint}?{query_filter}"
        data = self._get(url)
        try:
            filt_data = data["value"][0]
        except KeyError:
            raise OrchestratorProcessScheduleNotFound(
                message="Process schedule not found", error_message=f"Process with id {id} does not appear to exist.")
        return ProcessSchedule(self.client_id, self.refresh_token, self.tenant_name, self.folder_id, self.session, filt_data["Id"], filt_data["Name"], access_token=self.access_token)

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

    def get_jobs(self, top="100", options=None):
        """
        Returns the jobs of a given folder

        :param top : maximum number of results (100 default)
        :param options: dictionary of odata filtering options
        """
        endpoint = "/Jobs"
        default = {"$orderby": "StartTime desc", "$top": f"{top}"}
        enc_default = urlencode(default)
        if options:
            default.update(options)
            query_params = urlencode(default)
            url = f"{self.base_url}{endpoint}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}?{enc_default}"
        data = self._get(url)["value"]
        return [Job(self.client_id, self.refresh_token, self.tenant_name, self.id, self.name, self.session, job["Id"], job["Key"], job["ReleaseName"], access_token=self.access_token) for job in data]

    def get_job_keys(self, top="100", options=None):
        """

        """
        jobs = self.get_jobs(top, options)
        ids = {}
        for job in jobs:
            ids.update({job.key: job.name})
        return ids

    def get_job_by_key(self, key):
        endpoint = "/Jobs"
        query_param = urlencode({"$filter": f"Key eq {key}"})
        url = f"{self.base_url}{endpoint}?{query_param}"
        try:
            data = self._get(url)["value"][0]
        except IndexError:
            raise OrchestratorJobNotFound(
                message="Job not found", error_message=f"Job with key {key} does not appear to exist in the current folder.")
        return Job(self.client_id, self.refresh_token, self.tenant_name, self.id, self.name, self.session, data["Id"], data["Key"], data["ReleaseName"], access_token=self.access_token)

    def job_triggers(self, options=None):
        endpoint = "/JobTriggers"
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}"
        return self._get(url)["value"]

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
        return [Process(self.client_id, self.refresh_token, self.tenant_name, self.folder_id, self.session, process["Id"], process["Title"], process["Version"], process["Key"], access_token=self.access_token) for process in processes]

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
            "$filter": f"Key eq '{process_key}'"
        })
        endpoint = "/Processes"
        url = f"{self.base_url}{endpoint}?{query_param}"
        try:
            process = self._get(url)["value"][0]
        except IndexError:
            raise OrchestratorProcessNotFound(message="Process not found.",
                                              error_message=f"Process with key {process_key} does not appear to exist in the current folder.")
        return Process(self.client_id, self.refresh_token, self.tenant_name, self.folder_id,
                       self.session, process["Id"], process["Title"], process["Version"], process["Key"], access_token=self.access_token)

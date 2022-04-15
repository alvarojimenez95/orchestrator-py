from datetime import datetime
import queue
from urllib.parse import urlencode
from py import process
import requests
import random
import json
import string
from pprint import pprint

from orchestrator.exceptions import OrchestratorAuthException, OrchestratorMissingParam


class Orchestrator(object):
    """
    Base class from which the rest of the items, Robots, Folders,
    Assets will inherit. This class will containing the internal calls
    and the http methods, as well as the authentication method
    """

    cloud_url = "https://cloud.uipath.com"
    account_url = "https://account.uipath.com"
    oauth_endpoint = "/oauth/token"
    _now = datetime.now()
    _token_expires = datetime.now()
    _access_token = None

    def __init__(
        self,
        client_id=None,
        refresh_token=None,
        tenant_name=None,
        folder_id=None,
        session=None

    ):
        if not client_id or not refresh_token:
            raise OrchestratorAuthException(
                value=None, message="client id and refresh token cannot be left empty"
            )
        else:
            self.client_id = client_id
            self.refresh_token = refresh_token
            self.folder_id = folder_id
            self.tenant_name = tenant_name
            self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
        if session:
            self.session = session
        else:
            self.session = requests.Session()

    # @property
    # def folder_id(self):
    #     return self.folder_id

    # @folder_id.setter
    # def folder_id(self, value):
    #     self.folder_id = value

    @staticmethod
    def generate_reference():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def _get_token(self):
        body = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": self.refresh_token,
        }
        headers = {"Content-Type": "application/json"}
        url = f"{self.account_url}{self.oauth_endpoint}"
        try:
            r = requests.post(url=url, data=json.dumps(body), headers=headers)
            token_data = r.json()
            token = token_data["access_token"]
            expiracy = token_data["expires_in"]
            self._access_token = token
            self._token_expires = expiracy
        except Exception as err:
            print(err)

    def _auth_header(self):
        return {"Authorization": f"Bearer {self._access_token}"}

    @staticmethod
    def _content_header():
        return {"Content-Type": "application/json"}

    def _folder_header(self):
        if not self.folder_id:
            raise OrchestratorAuthException(value="folder id", message="folder cannot be null")
        return {"X-UIPATH-OrganizationUnitId": f"{self.folder_id}"}

    def _internal_call(self, method, endpoint, *args, **kwargs):
        pprint(self.folder_id)
        self._get_token()
        headers = self._auth_header()
        if method == "POST":
            headers.update(self._content_header())
        if self.folder_id:
            headers.update(self._folder_header())
        try:
            # print(endpoint)
            if kwargs:
                # pprint(kwargs)
                item_data = kwargs['body']['body']
                # print(json.dumps(item_data))
                r = requests.request(method, endpoint, json=item_data, headers=headers)
            else:
                r = requests.request(method, endpoint, headers=headers)
            # print(endpoint)
            # pprint(r)
            return r.json()
        except Exception as err:
            print(err)

    def _get(self, url, *args, **kwargs):

        return self._internal_call("GET", url, args, kwargs)

    def _post(self, url, *args, **kwargs):
        # pprint(kwargs)
        return self._internal_call("POST", url, args, body=kwargs)

    def _put(self, url, *args, **kwargs):
        return self._internal_call("PUT", url, args, body=kwargs)

    def _delete(self, url, *args, **kwargs):
        return self._internal_call("DELETE", url, args, kwargs)

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


class Folder(Orchestrator):
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

    def info(self):
        """Returns a information of a single
            folder based on its folder id
        """
        endpoint = f"/Folders({self.id})"
        url = f"{self.base_url}{endpoint}"
        data = self._get(url)
        return data

    def get_all_queues(self, options=None):
        """
            Parameters:
            :param options (dict(str, any)) dictionary of
            filtering odata options
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
        queues = self.get_all_queues(options)
        ids = {}
        for queue in queues:
            ids.update({queue.id: queue.name})
        return ids

    def get_queue_processing_records(self, options=None):
        """
            Returns a list of queue processing records for all the queues

            :options dictionary for odata options

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

    def get_all_assets(self, options=None):
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
        pprint(data)
        pprint(self.id)
        filt_data = data['value']
        return [Asset(self.client_id, self.refresh_token, self.tenant_name, self.id, self.name, self.session, asset["Id"], asset["Name"]) for asset in filt_data]

    def get_asset_ids(self, options=None):
        """
            Returns a dictionary of ky value pairs
                key: asset name
                value: asset id
            Parameters:
                :options dict of odata filter options
        """
        assets = self.get_all_assets(options)
        return [{asset['Name']: asset['Id']} for asset in assets]

    def create_asset(self, body=None):
        pass


class Queue(Folder):
    """
        To initialize a class you need the folder id because queues are
        dependant on the folder id
    """

    def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, folder_name=None, session=None, queue_name=None, queue_id=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, tenant_name=tenant_name, folder_id=folder_id, folder_name=folder_name, session=session)
        if not queue_id:
            raise OrchestratorMissingParam(value="queue_id",
                                           message="Required parameter(s) missing: queue_id")
        self.id = queue_id
        self.name = queue_name
        self.folder_name = folder_name
        self.folder_id = folder_id
        self.tenant_name = tenant_name
        self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
        if session:
            self.session = session
        else:
            self.session = requests.Session()

    def info(self):
        """
            Gets a single queue by queue id
        """
        endpoint = f"/QueueDefinitions({self.id})"
        url = f"{self.base_url}{endpoint}"
        data = self._get(url)
        return data

    def get_processing_records(self, num_days=0, options=None):
        """
            Returns a list of processing records for a given
            queue and a certain number of days (0 by default)

            :options dictionary for odata options
        """
        endpoint = "/QueueProcessingRecords"
        query = f"daysNo={num_days},queueDefinitionId={self.id}"
        uipath_svc = f"/UiPathODataSvc.RetrieveLastDaysProcessingRecords({query})"
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}{uipath_svc}"
        data = self._get(url)
        return data['value']

    def get_item_by_id(self, item_id):
        """
            Gets a single item by item id

            Parameters:

            :param item_id : item id


            Necesito una clase Item
        """
        return QueueItem(self.client_id, self.refresh_token, self.tenant_name, self.folder_id, self.folder_name, self.name, self.id, self.session, item_id)

    def get_queue_items(self, options=None):
        """
            Returns a list of queue items belonging to a given queue
            Parameters:
                :param queue_id : the queue id
                :param options dict: odata options, $filter tag will be overwritten
        """
        endpoint = "/QueueItems"
        odata_filter = {"$Filter": f"QueueDefinitionId eq {self.id}"}
        if options:
            odata_filter.update(options)
        query_params = urlencode(odata_filter)
        url = f"{self.base_url}{endpoint}?{query_params}"
        data = self._get(url)
        filt_data = data['value']
        # pprint(filt_data)[0]
        return [QueueItem(self.client_id, self.refresh_token, self.tenant_name, self.folder_id, self.folder_name, self.name, self.id, session=self.session, item_id=item["Id"]) for item in filt_data]

    def get_queue_items_ids(self, options=None):
        """
            Returns a list of dictionaries where the key value
            pairse ar <queue_id : item_id>
        """
        items = self.get_queue_items(options)
        ids = {}
        for item in items:
            ids.update({item.id: item.queue_name})
        return ids

    def create_queue_item(self, queue_id, specific_content=None, priority="Low"):
        """
            Creates a new Item

            Parameters:
                :param queue_id - the queue id
                :specific_content - python dictionary of key value pairs. It does not
                                    admit nested dictionaries. If you want to be able to
                                    pass a dictionary as a key value pair inside the specific
                                    content attribute, you need to json.dumps(dict) first for it
                                    to work.
                :param priority - sets up the priority (Low by default)
        """
        endpoint = "/Queues"
        uipath_svc = "/UiPathODataSvc.AddQueueItem"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        if not specific_content:
            raise OrchestratorMissingParam(value="specific_content", message="specific content cannot be null")
        queue_name = self.get_queue(queue_id=queue_id)["Name"]
        format_body_queue = {
            "itemData": {
                "Priority": priority,
                "Name": queue_name,
                "SpecificContent": specific_content,
                "Reference": self.generate_reference(),
                "Progress": "New"
            }
        }
        # pprint(format_body_queue)
        return self._post(url, body=format_body_queue)

    def _format_specific_content(self, queue_name, sp_content, priority="Low"):
        formatted_sp_content = {
            "Name": queue_name,
            "Priority": priority,
            "SpecificContent": sp_content,
            "Reference": self.generate_reference(),
            "Progress": "New"
        }
        return formatted_sp_content

    def bulk_create_items(self, queue_id, specific_contents=None, priority="Low"):
        """
            Creates a list of items for a given queue

            Parameters: 
                :param queue_id - the queue id 
                :specific_content - python dictionary of key value pairs. It does not 
                                    admit nested dictionaries. If you want to be able to 
                                    pass a dictionary as a key value pair inside the specific
                                    content attribute, you need to json.dumps(dict) first for it
                                    to work.
                :param priority - sets up the priority (Low by default)
        """
        endpoint = "/Queues"
        uipath_svc = "/UiPathODataSvc.BulkAddQueueItems"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        if not specific_contents:
            raise OrchestratorMissingParam(value="specific_contents", message="specific contents cannot be null")
        queue_name = self.get_queue(queue_id=queue_id)["Name"]
        format_body_queue = {
            "commitType": "StopOnFirstFailure",
            "queueName": queue_name,
            "queueItems": [self._format_specific_content(queue_name=queue_name, sp_content=sp_content) for sp_content in specific_contents]
        }
        # pprint(format_body_queue)
        return self._post(url, body=format_body_queue)

    def edit_queue(self, name=None, description=None):
        if not name:
            raise OrchestratorMissingParam(value="name", message="name cannot be null")
        endpoint = f"/QueueDefinitions({self.id})"
        url = f"{self.base_url}{endpoint}"
        format_body_queue = {
            "Name": name,
            "Description": description
        }
        return self._put(url, body=format_body_queue)

    def delete_queue(self):
        endpoint = f"/QueueDefinitions({self.id})"
        url = f"{self.base_url}{endpoint}"
        return self._delete(url)


class QueueItem(Queue):
    def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, folder_name=None, queue_name=None, queue_id=None, session=None, item_id=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, tenant_name=tenant_name, folder_id=folder_id,
                         folder_name=folder_name, queue_name=queue_name, queue_id=queue_id, session=session)
        if not item_id:
            raise OrchestratorMissingParam(value="item id",
                                           message="Required parameter(s) missing: item_id")
        self.tenant_name = tenant_name
        self.folder_id = folder_id
        self.folder_name = folder_name
        self.queue_name = queue_name
        self.queue_id = queue_id
        self.id = item_id

        self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
        if session:
            self.session = session
        else:
            self.session = requests.Session()

    def content(self):
        info = self.info()
        return info["SpecificContent"]

    def info(self):
        """
            Gets a single item by item id

            Parameters:

            :param item_id : item id


            Necesito una clase Item
        """
        endpoint = f"/QueueItems({self.id})"
        url = f"{self.base_url}{endpoint}"
        return self._get(url)

    def delete(self):
        """
            Deletes the given queue item
        """
        endpoint = f"/QueueItems({self.id})"
        url = f"{self.base_url}{endpoint}"
        return self._delete(url)

    def edit(self, body=None):
        """
            edits the given queue item
        """
        endpoint = f"/QueueItems({self.id})"
        url = f"{self.base_url}{endpoint}"
        return self._put(url, body=body)

    def last_entry(self):
        """
            Returns the last entry of the given 
            queue item
        """
        endpoint = f"/QueueItems({self.id})"
        uipath_svc = "/UiPath.Server.Configuration.OData.GetItemLastRetry"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        return self._get(url)

    def history(self):
        """
            Returns the history of the given queue
            item
        """
        endpoint = f"/QueueItems({self.id})"
        uipath_svc = "/UiPathODataSvc.GetItemProcessingHistory"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        return self._get(url)["value"]

    def update_status(self, status=None):
        """
            Updates the progress field of a given queue
            item (note: it must be already In Progress)
        """
        if not status:
            raise OrchestratorMissingParam(value="status", message="status cannot be None")
        endpoint = f"/QueueItems({self.self.id})"
        uipath_svc = "/UiPathODataSvc.SetTransactionProgress"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        body = {
            "progress": status
        }
        return self._post(url, body=body)

    def events(self):
        """
            Gets tue item events associated to the current 
            queue item 

            No funciona no se por que
        """
        endpoint = "/QueueItemEvents"
        uipath_svc = f"/UiPathODataSvc.GetQueueItemEventsHistory(queueItemId={{self.id}})"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        return self._get(url)

    # falta uno de get_queue_item_comments


class QueueItemComment(QueueItem):
    def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, folder_name=None, queue_name=None, queue_id=None, session=None, item_id=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, folder_id=folder_id,
                         folder_name=folder_name, queue_name=queue_name, queue_id=queue_id, session=session)
        if item_id:
            raise OrchestratorMissingParam(value="item id",
                                           message="Required parameter(s) missing: item_id")
        self.tenant_name = tenant_name
        self.folder_id = folder_id
        self.queue_id = queue_id
        self.item_it = item_id
        self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
        if session:
            self.session = session
        else:
            self.session = requests.Session()

    def info(self):
        """
            Returns the info of the current item 
            comment
        """
        endpoint = f"/QueueItemComments({self.item_id})"
        url = f"{self.base_url}{endpoint}"
        return self._get(url)

    def delete(self):
        """
            Deletes the current queue item comment
        """
        endpoint = f"/QueueItemComments({self.item_id})"
        url = f"{self.base_url}{endpoint}"
        return self._delete(url)

    def create(self, body=None):
        """
            Creates a new queue item comment
        """
        endpoint = f"/QueueItemComments({self.item_id})"
        url = f"{self.base_url}{endpoint}"
        return self._put(url, body=body)


class Asset(Folder):
    def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, folder_name=None, session=None, asset_id=None, asset_name=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, tenant_name=tenant_name, folder_id=folder_id, folder_name=folder_name, session=session)
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
        endpoint = f"/Assets({self.asset_id})"
        url = f"{self.base_url}{endpoint}"
        return self._get(url)

    def edit(self, body=None):
        endpoint = f"/Assets({self.asset_id})"
        url = f"{self.base_url}{endpoint}"
        return self._put(url, body=body)

    def delete(self, body=None):
        endpoint = f"/Assets({self.asset_id})"
        url = f"{self.base_url}{endpoint}"
        return self._delete(url, body=body)


class ProcessSchedule(Orchestrator):
    def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, session=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, folder_id=folder_id)
        if not tenant_name or not folder_id:
            raise OrchestratorMissingParam(value="tenant_name, folder_id",
                                           message="Required parameter(s) missing: tenant_name, folder_id")
        self.tenant_name = tenant_name
        self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
        if session:
            self.session = session
        else:
            self.session = requests.Session()

    def get_all_schedules(self, options=None):
        """
            Returns all process schedules
        """
        endpoint = "/ProcessSchedules"
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}"
        data = self._get(url)
        return data['value']

    def get_schedule_ids(self, options=None):
        """
            Returns a list of dictionaries 
                name -- schedule_id
        """
        process_schedules = self.get_all_schedules(options=options)
        return [{schedule["Name"]: schedule["Id"] for schedule in process_schedules}]

    def get_robot_ids(self, schedule_id=None, options=None):
        endpoint = "/ProcessSchedules"
        uipath_svc = f"/UiPath.Server.Configuration.OData.GetRobotIdsForSchedule(key = {schedule_id})"
        if not schedule_id:
            raise OrchestratorMissingParam(value="schedule_id", message="schedule id parameter is required")
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}{uipath_svc}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}{uipath_svc}"
        data = self._get(url)
        return data['value']

    def enable_process_schedule(self, enable: bool = False, schedule_ids=[]):
        if not len(schedule_ids):
            raise OrchestratorMissingParam(value="schedule_ids", message="At least un schedule id needs to be provided.")
        else:
            endpoint = "/ProcessSchedules"
            uipath_svc = "/UiPath.Server.Configuration.OData.SetEnabled"
            body = {
                "enabled": enable,
                "scheduleIds": schedule_ids
            }
            url = f"{self.base_url}{endpoint}{uipath_svc}"
            return self._post(url, body=body)


class Process(Orchestrator):
    def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, session=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, folder_id=folder_id)
        if not tenant_name or not folder_id:
            raise OrchestratorMissingParam(value="tenant_name, folder_id",
                                           message="Required parameter(s) missing: tenant_name, folder_id")
        self.tenant_name = tenant_name
        self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
        if session:
            self.session = session
        else:
            self.session = requests.Session()

    def get_all_processes(self, options=None):
        """
            Returns a list of all processes
        """
        endpoint = "/Processes"
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}"

        data = self._get(url)
        return data['value']

    def get_processes_key(self, options=None):
        """
            Returns a dictionary 
                process title -- process key
        """
        processes = self.get_all_processes(options=options)
        return [{process["Title"]: process["Key"]} for process in processes]

    def download_process_package(self, process_key):
        """
            Doesnt work
        """
        endpoint = "/Processes"
        uipath_svc = f"UiPath.Server.Configuration.OData.DownloadPackage(key='{process_key}')"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        return self._get(url)

    def get_available_versions(self, process_key):
        """
        Gets all the available versions for a given process
        """
        endpoint = "/Processes"
        uipath_svc = f"/UiPath.Server.Configuration.OData.GetProcessVersions(processId='{process_key}')"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        return self._get(url)

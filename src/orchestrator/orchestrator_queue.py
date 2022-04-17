from orchestrator.exceptions import OrchestratorMissingParam
from orchestrator.orchestrator_http import OrchestratorHTTP
import requests
from urllib.parse import urlencode
from orchestrator.orchestrator_queue_item import QueueItem

__all__ = ["Queue"]


class Queue(OrchestratorHTTP):
    """
        To initialize a class you need the folder id because queues are
        dependant on the folder id
    """

    def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, folder_name=None, session=None, queue_name=None, queue_id=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, tenant_name=tenant_name, folder_id=folder_id, session=session)
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

    def __str__(self):
        return f"Queue Id: {self.id} \nQueue Name: {self.name} \nFolder Id: {self.folder_id} \nFolder Name: {self.folder_name}"

    def info(self):
        """
            Gets a single queue by queue id
        """
        endpoint = f"/QueueDefinitions({self.id})"
        url = f"{self.base_url}{endpoint}"
        data = self._get(url)
        return data

    def get_processing_records(self, num_days=1, options=None):
        """
            Returns a list of processing records for a given
            queue and a certain number of days (by default, hourly reports
            from the last day)

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
            Maximum number of results: 1000
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
        format_body_queue = {
            "itemData": {
                "Priority": priority,
                "Name": self.name,
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
        format_body_queue = {
            "commitType": "StopOnFirstFailure",
            "queueName": self.name,
            "queueItems": [self._format_specific_content(queue_name=self.name, sp_content=sp_content) for sp_content in specific_contents]
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

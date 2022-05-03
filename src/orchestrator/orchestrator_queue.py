from uuid import uuid4
from orchestrator.exceptions import OrchestratorMissingParam
from orchestrator.orchestrator_http import OrchestratorHTTP
import requests
from urllib.parse import urlencode
from orchestrator.orchestrator_queue_item import QueueItem

__all__ = ["Queue"]


class Queue(OrchestratorHTTP):
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
            Returns information about the queue

            @returns: dictionary with more in depth information
            about the queue 
        """
        endpoint = f"/QueueDefinitions({self.id})"
        url = f"{self.base_url}{endpoint}"
        data = self._get(url)
        return data

    def start(self, machine_identifier, specific_content):
        """
            Starts a given transaction

            @machine_identifier: the machine's unique identifier
            @specific_content: the specific content of the transaction
        """
        endpoint = "/Queues/UiPathODataSvc.StartTransaction"
        format_body_start = {
            "transactionData": {
                "Name": self.name,
                "RobotIdentifier": machine_identifier,
                "SpecificContent": specific_content
            }
        }
        url = f"{self.base_url}{endpoint}"
        return self._post(url, body=format_body_start)

    def get_processing_records(self, num_days=1, options=None):
        """
            Returns a list of processing records for a given
            queue and a certain number of days (by default, hourly reports
            from the last day)

            @num_days: the number of days before today from which to get
            the processing records (default: 1)
            @options: dictionary of odata filtering options
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
            Gets a single Item by item id

            @item_id: the id of the item
            ========
            @returns: an Item object with the specified item id
        """
        return QueueItem(self.client_id, self.refresh_token, self.tenant_name, self.folder_id, self.folder_name, self.name, self.id, self.session, item_id)

    def get_queue_items(self, options=None):
        """
            Returns a list of queue items of the given queue

            @options: dictionary of odata filtering options ($filter tag will be overwritten)
            =========
            @returns: a list of QueueItem objects of the given queue (Maximum number of results: 1000)
        """
        endpoint = "/QueueItems"
        odata_filter = {"$Filter": f"QueueDefinitionId eq {self.id}"}
        if options:
            odata_filter.update(options)
        query_params = urlencode(odata_filter)
        url = f"{self.base_url}{endpoint}?{query_params}"
        data = self._get(url)
        filt_data = data['value']
        return [QueueItem(self.client_id, self.refresh_token, self.tenant_name, self.folder_id, self.folder_name, self.name, self.id, session=self.session, item_id=item["Id"]) for item in filt_data]

    def get_queue_items_ids(self, options=None):
        """
            Returns a list of dictionaries with the queue 
            item ids 

            @options: dictionary of odata filtering options 
            ========
            @returns: a dictionary where the keys are the queue item
            ids of the given queue and the values the queue name
        """
        items = self.get_queue_items(options)
        ids = {}
        for item in items:
            ids.update({item.id: item.queue_name})
        return ids

    def add_queue_item(self, specific_content=None, priority="Low"):
        """Creates a new Item

            @specific_content: dictionary of key value pairs (it does not
            admit nested dictionaries; for it to work json.dumps first)

            @priority - sets up the priority (Low by default)
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
                # "Progress": "In Progres"
            }
        }
        # pprint(format_body_queue)
        return self._post(url, body=format_body_queue)

    def _format_specific_content(self, queue_name, sp_content, priority="Low", progress="New", reference=None):
        formatted_sp_content = {
            "Name": queue_name,
            "Priority": priority,
            "SpecificContent": sp_content,
            "Progress": progress
        }
        if reference:
            ran_uuid = str(uuid4())
            ref_uuid = {"Reference": f"{sp_content[reference]}#{ran_uuid}"}
            formatted_sp_content.update(ref_uuid)
        else:
            formatted_sp_content.update(ran_uuid)

        return formatted_sp_content

    def bulk_create_items(self, specific_contents=None, priority="Low", progress="New", reference=None):
        """Adds a list of items for a given queue
            @param specific_content: dictionary of key value pairs. It does not
            admit nested dictionaries. If you want to be able to pass a dictionary 
            as a key value pair inside the specific content attribute, you need to 
                                json.dumps(dict) 
            first for it to work.
            @priority: sets up the priority (default: Low)
            @progress: sets up the progress bar (default: New)
            @reference: indicates a specific field of the specific content to
            be used as a queue reference.
        """
        endpoint = "/Queues"
        uipath_svc = "/UiPathODataSvc.BulkAddQueueItems"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        if not specific_contents:
            raise OrchestratorMissingParam(value="specific_contents", message="specific contents cannot be null")
        format_body_queue = {
            "commitType": "StopOnFirstFailure",
            "queueName": self.name,
            "queueItems": [self._format_specific_content(queue_name=self.name, sp_content=sp_content, priority=priority, progress=progress) for sp_content in specific_contents]
        }
        # pprint(format_body_queue)
        return self._post(url, body=format_body_queue)

    def edit_queue(self, name=None, description=None):
        """Edits the queue with a new name and a new 
        descriptions

        @name: the new name of the queue
        @description: the new description of the queue

        """
        if not name or not description:
            raise OrchestratorMissingParam(value="name/description", message="name and/or description cannot be null")
        endpoint = f"/QueueDefinitions({self.id})"
        url = f"{self.base_url}{endpoint}"
        format_body_queue = {
            "Name": name,
            "Description": description
        }
        return self._put(url, body=format_body_queue)

    def delete_queue(self):
        """Deletes the queue"""
        endpoint = f"/QueueDefinitions({self.id})"
        url = f"{self.base_url}{endpoint}"
        return self._delete(url)

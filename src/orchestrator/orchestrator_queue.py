import logging
from pprint import pprint
from uuid import uuid4
import uuid
import json
from orchestrator.exceptions import OrchestratorMissingParam
from orchestrator.orchestrator_http import OrchestratorHTTP
import requests
from urllib.parse import urlencode

from orchestrator.orchestrator_queue_item import QueueItem

__all__ = ["Queue"]


class Queue(OrchestratorHTTP):
    classes = ["Comments", "Status", "Reference", "SpecificContent"]
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

    def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, folder_name=None, session=None, queue_name=None, queue_id=None, access_token=None):
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
        self.access_token = access_token
        self.refresh_token = refresh_token
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

    def start(self, machine_identifier, specific_content=None, references=None, separator="-", fields=None):
        """
            Starts a given transaction

            @machine_identifier: the machine's unique identifier
            @specific_content: the specific content of the transaction
            @reference: a reference from the specific content
            @fields: a dictionary of additional fields to be added to the specific content
        """
        ran_uuid = str(uuid4())
        batch_id = str(uuid.uuid4())
        logging.debug("Starting new transaction")
        endpoint = "/Queues/UiPathODataSvc.StartTransaction"
        format_body_start = {
            "transactionData": {
                "Name": self.name,
                "RobotIdentifier": machine_identifier,
                "SpecificContent": specific_content,
            }
        }
        if references:
            try:
                ref = ""
                for reference in references:
                    value = format_body_start["transactionData"]["SpecificContent"][reference]
                    ref += str(value)+separator
                format_body_start["transactionData"]["Reference"] = f"{ref[:-1]}#{batch_id}"
            except KeyError as err:
                if reference in err.args:
                    logging.error(f"Invalid reference: {reference} not found in SpecificContent")
                    raise Exception(f"Invalid reference: {reference} not found in SpecificContent")
            format_body_start["transactionData"]["SpecificContent"]["ItemID"] = value
            format_body_start["transactionData"]["SpecificContent"]["ReferenceID"] = ran_uuid
            format_body_start["transactionData"]["SpecificContent"]["BatchID"] = batch_id
        if fields:
            format_body_start["transactionData"]["SpecificContent"].update(fields)

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
        return QueueItem(self.client_id, self.refresh_token, self.tenant_name, self.folder_id, self.folder_name, self.name, self.id, self.session, item_id, access_token=self.access_token)

    def get_queue_items(self, options=None):
        """
            Returns a list of queue items of the given queue

            @options: dictionary of odata filtering options ($filter tag will be overwritten)
            =========
            @returns: a list of QueueItem objects of the given queue (Maximum number of results: 1000)
        """
        endpoint = "/QueueItems"
        if options and ("$filter" in options):
            print(options["$filter"])
            odata_filter = {"$filter": f"{options['$filter']} and QueueDefinitionId eq {self.id}"}
        else:
            odata_filter = {"$filter": f"QueueDefinitionId eq {self.id} and Status in ('Abandoned', 'Deleted') eq false"}

        query_params = urlencode(odata_filter)
        url = f"{self.base_url}{endpoint}?{query_params}"
        data = self._get(url)
        pprint(data)
        filt_data = data['value']
        return [QueueItem(self.client_id, self.refresh_token, self.tenant_name, self.folder_id, self.folder_name, self.name, self.id, session=self.session, item_id=item["Id"], content=item["SpecificContent"], reference=item["Reference"], access_token=self.access_token) for item in filt_data]

    def get_queue_items_by_status(self, status):
        """
        Returns a list of QueueItems with the status
        as indicated in the argument.
        """
        endpoint = "/QueueItems"
        odata_filter = {"$filter": f"QueueDefinitionId eq {self.id} and Status eq '{status}'"}
        query_params = urlencode(odata_filter)
        url = f"{self.base_url}{endpoint}?{query_params}"
        data = self._get(url)
        filt_data = data['value']
        return [QueueItem(self.client_id, self.refresh_token, self.tenant_name, self.folder_id, self.folder_name, self.name, self.id, session=self.session, item_id=item["Id"], content=item["SpecificContent"], reference=item["Reference"], access_token=self.access_token) for item in filt_data]

    def _get_sp_contents(self, options=None):
        items = self.get_queue_items(options=options)
        contents = []
        for item in items:
            contents.append(item.content)
        return contents

    def _get_references(self, options=None):
        items = self.get_queue_items(options=options)
        references = []
        for item in items:
            references.append(item.reference)
        return references

    def check_duplicate(self, reference):
        """
        Given a queue reference, it checks whether a given queue
        has already appeared in the queue once.

        Parameters:

            - `param` reference: the reference or part of it of the new queue item

        Returns:
            If a reference is found in the queue with the given status, it returns the first
            item whose reference matches the one indicated as an argument. Otherwise it returns
            False.
        """
        filt_items = self.get_queue_items(options={"$filter": f"contains(Reference, '{reference}') and Status eq 'Successful'"})

        if len(filt_items) > 0:
            return filt_items[0]
        else:
            return False

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

    def _format_specific_content(self, sp_content, reference=None, priority="Low", progress="New", batch_id=None):
        ran_uuid = str(uuid4())

        if reference:
            try:
                ref_uuid = {"Reference": f"{sp_content[reference]}#{batch_id}"}
                sp_content.update({"ReferenceID": ran_uuid})
                sp_content.update({"BatchID": batch_id})
                sp_content.update({"ItemID": sp_content[reference]})
                formatted_sp_content = {
                    "Name": self.name,
                    "Priority": priority,
                    "SpecificContent": sp_content,
                    "Progress": progress,
                }
                formatted_sp_content.update(ref_uuid)
                return formatted_sp_content
            except KeyError as err:
                if reference in err.args:
                    raise Exception(f"Invalid reference: {reference} not found in sp_content")
        else:
            ref_uuid = {"Reference": f"{ran_uuid}"}
            sp_content.update({"ReferenceID": ran_uuid})
            sp_content.update({"BatchID": batch_id})
            formatted_sp_content = {
                "Name": self.name,
                "Priority": priority,
                "SpecificContent": sp_content,
                "Progress": progress,
            }
            formatted_sp_content.update(ref_uuid)
            return formatted_sp_content

    def _format_dataframe(self, df):
        specific_contents = []
        for i in df.index:
            specific_contents.append(df.iloc[i].to_json())
        # pprint(specific_contents)
        return specific_contents

    def bulk_dataframe(self, df, priority="Low", progress="New", reference=None):
        """Adds a dataframe of items to a given queue"""
        endpoint = "/Queues"
        uipath_svc = "/UiPathODataSvc.BulkAddQueueItems"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        sp_contents = self._format_dataframe(df=df)
        batch_id = str(uuid4())
        format_body_queue = {
            "commitType": "StopOnFirstFailure",
            "queueName": self.name,
            "queueItems": [self._format_specific_content(sp_content=json.loads(sp_content), reference=reference, priority=priority, progress=progress, batch_id=batch_id) for sp_content in sp_contents]
        }
        # pprint(format_body_queue)
        return self._post(url, body=format_body_queue)

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

            Specific Content includes by default the following columns:
                - BatchID: representing a unique ID for the specific batch of items to be uploaded
                - ReferenceID: a unique ID of the item
                - ItemID: if reference is set to true, ads a new field with the reference
        """
        endpoint = "/Queues"
        uipath_svc = "/UiPathODataSvc.BulkAddQueueItems"
        print(type(specific_contents[0]))
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        if not specific_contents:
            raise OrchestratorMissingParam(value="specific_contents", message="specific contents cannot be null")

        batch_id = str(uuid4())
        format_body_queue = {
            "commitType": "StopOnFirstFailure",
            "queueName": self.name,
            "queueItems": [self._format_specific_content(sp_content=sp_content, reference=reference, priority=priority, progress=progress, batch_id=batch_id) for sp_content in specific_contents]
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

    def get_queue_item_comments(self, q=None):
        endpoint = "/QueueItemComments"
        if q:
            query_params = urlencode({
                "$filter": q
            })
            url = f"{self.base_url}{endpoint}?{query_params}"
        url = f"{self.base_url}{endpoint}"
        return self._get(url)

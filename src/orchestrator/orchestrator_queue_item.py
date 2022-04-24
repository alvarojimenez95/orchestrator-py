from orchestrator.orchestrator_http import OrchestratorHTTP
from orchestrator.exceptions import OrchestratorMissingParam
import requests
from urllib.parse import urlencode
import json

__all__ = ["QueueItem"]


class QueueItem(OrchestratorHTTP):
    def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, folder_name=None, queue_name=None, queue_id=None, session=None, item_id=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, tenant_name=tenant_name, folder_id=folder_id,
                         session=session)
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

    def __str__(self):
        return f"Item Id: {self.id} \nQueue: {self.queue_name} \nFolder: {self.folder_name}"

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

    def set_transaction_progress(self, status=None):
        """
            Updates the progress field of a given queue
            item (note: it must be already In Progress)
        """
        if not status:
            raise OrchestratorMissingParam(value="status", message="status cannot be None")
        endpoint = f"/QueueItems({self.id})"
        uipath_svc = "/UiPathODataSvc.SetTransactionProgress"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        body = {
            "progress": status
        }
        return self._post(url, body=body)

    def set_transaction_status(self, success: bool, reason=None, exception_type=None):
        endpoint = f"/Queues({self.id})"
        uipath_svc = "/UiPathODataSvc.SetTransactionResult"
        transaction_body = {
            "transactionResult": {
                "IsSuccessful": True,

            }
        }
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        return self._post(url, body=transaction_body)

    def events(self):
        """
            Gets queue item events associated to the current
            queue item

            No funciona no se por que
        """
        endpoint = "/QueueItemEvents"
        uipath_svc = f"/UiPathODataSvc.GetQueueItemEventsHistory(queueItemId={{self.id}})"
        url = f"{self.base_url}{endpoint}{uipath_svc}"
        return self._get(url)

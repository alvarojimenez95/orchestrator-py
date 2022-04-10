from datetime import datetime
from urllib.parse import urlencode
import requests
import json


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
        folder_id=None,

    ):
        if not client_id or not refresh_token:
            raise OrchestratorAuthException(
                value=None, message="client id and refresh token cannot be left empty"
            )
        else:
            self.client_id = client_id
            self.refresh_token = refresh_token
            self.folder_id = folder_id

    @staticmethod
    def expiracy_date(seconds: str):

        pass

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

    def _folder_header(self):
        if not self.folder_id:
            raise OrchestratorAuthException(value="folder id", message="folder cannot be null")
        return {"X-UIPATH-OrganizationUnitId": f"{self.folder_id}"}

    def _internal_call(self, method, endpoint, *args, **kwargs):

        self._get_token()
        headers = self._auth_header()
        encoded_params = None

        if self.folder_id:
            headers.update(self._folder_header())
        try:
            print(endpoint)
            r = requests.request(method, endpoint, data=json.dumps(kwargs), params=encoded_params, headers=headers)
            print(r)
            return r.json()
        except Exception as err:
            print(err)

    def _get(self, endpoint, *args, **kwargs):
        if args:
            kwargs.update(args)
        return self._internal_call("GET", endpoint, args, kwargs)


class Folder(Orchestrator):
    def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, session=None):
        super().__init__(client_id=client_id, refresh_token=refresh_token, folder_id=folder_id)
        if not tenant_name:
            raise OrchestratorMissingParam(value="tenant_name",
                                           message="Required parameter missing: tenant_name")

        self.tenant_name = tenant_name
        self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
        if session:
            self.session = session
        else:
            self.session = requests.Session()

    def get_all_folders(self, filter=None, expand=None, select=None):
        """
            Gets all the folders from a given Organization Unit
        """
        endpoint = "/Folders"
        url = f"{self.base_url}{endpoint}"
        print(url)
        data = self._get(url)
        return data['value']

    def get_folder_ids(self, filter=None, expand=None, select=None):
        """
            Returns a python list of dictionaries
            with all the folder names as keys
            and the folder ids as values
        """
        folders = self.get_all_folders()
        ids = []
        for folder in folders:
            ids.append({folder['DisplayName']: folder['Id']})
        return ids

    def get_folder(self, folder_id):
        """Returns a single folder based on 
            its folder id
        """
        endpoint = f"/Folders({folder_id})"
        url = f"{self.base_url}{endpoint}"
        data = self._get(url)
        return data


class Queue(Orchestrator):
    """
        To initialize a class you need the folder id because queues are
        dependant on the folder id
    """

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

    def get_all_queues(self, options=None):
        """
            :param options (dict(str, any)) dictionary of 
            filtering odata options
        """
        endpoint = "/QueueDefinitions"
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}?{query_params}"
        data = self._get(url)
        return data['value']

    def get_queue_ids(self, options=None):
        """
            Returns a list of dictionaries containing
            the queue name and the queue id

            :options dictionary for odata options

        """
        queues = self.get_all_queues(options)['value']
        queue_ids = [{queue['Name']: queue['Id']} for queue in queues]
        return queue_ids

    def get_queue(self, queue_id):
        endpoint = f"/QueueDefinitions({queue_id})"
        url = f"{self.base_url}{endpoint}"
        data = self._get(url)
        return data

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

    def get_processing_records(self, queue_id, num_days=0, options=None):
        """
            Returns a list of processing records for a given 
            queue and a certain number of days (0 by default)

            :options dictionary for odata options
        """
        endpoint = "/QueueProcessingRecords"
        query = f"daysNo={num_days},queueDefinitionId={queue_id}"
        uipath_svc = f"/UiPathODataSvc.RetrieveLastDaysProcessingRecords({query})"
        if options:
            query_params = urlencode(options)
            url = f"{self.base_url}{endpoint}?{query_params}"
        else:
            url = f"{self.base_url}{endpoint}{uipath_svc}"
        data = self._get(url)
        return data['value']


class Asset(Orchestrator):
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
        return data['value']

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

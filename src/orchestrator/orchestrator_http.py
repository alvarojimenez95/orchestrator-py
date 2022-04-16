from datetime import datetime
import requests
import random
import json
import string
from pprint import pprint

from orchestrator.exceptions import OrchestratorAuthException, OrchestratorMissingParam


class OrchestratorHTTP(object):
    cloud_url = "https://cloud.uipath.com"
    account_url = "https://account.uipath.com"
    oauth_endpoint = "/oauth/token"
    _now = datetime.now()
    _token_expires = datetime.now()
    _access_token = None

    def __init__(
        self,
        client_id,
        refresh_token,
        tenant_name,
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

    # falta uno de get_queue_item_comments


# class QueueItemComment(QueueItem):
#     def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, folder_name=None, queue_name=None, queue_id=None, session=None, item_id=None):
#         super().__init__(client_id=client_id, refresh_token=refresh_token, folder_id=folder_id,
#                          folder_name=folder_name, queue_name=queue_name, queue_id=queue_id, session=session)
#         if item_id:
#             raise OrchestratorMissingParam(value="item id",
#                                            message="Required parameter(s) missing: item_id")
#         self.tenant_name = tenant_name
#         self.folder_id = folder_id
#         self.queue_id = queue_id
#         self.item_it = item_id
#         self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
#         if session:
#             self.session = session
#         else:
#             self.session = requests.Session()

#     def info(self):
#         """
#             Returns the info of the current item
#             comment
#         """
#         endpoint = f"/QueueItemComments({self.item_id})"
#         url = f"{self.base_url}{endpoint}"
#         return self._get(url)

#     def delete(self):
#         """
#             Deletes the current queue item comment
#         """
#         endpoint = f"/QueueItemComments({self.item_id})"
#         url = f"{self.base_url}{endpoint}"
#         return self._delete(url)

#     def create(self, body=None):
#         """
#             Creates a new queue item comment
#         """
#         endpoint = f"/QueueItemComments({self.item_id})"
#         url = f"{self.base_url}{endpoint}"
#         return self._put(url, body=body)


# class ProcessSchedule(Orchestrator):
#     def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, session=None):
#         super().__init__(client_id=client_id, refresh_token=refresh_token, folder_id=folder_id)
#         if not tenant_name or not folder_id:
#             raise OrchestratorMissingParam(value="tenant_name, folder_id",
#                                            message="Required parameter(s) missing: tenant_name, folder_id")
#         self.tenant_name = tenant_name
#         self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
#         if session:
#             self.session = session
#         else:
#             self.session = requests.Session()

#     def get_all_schedules(self, options=None):
#         """
#             Returns all process schedules
#         """
#         endpoint = "/ProcessSchedules"
#         if options:
#             query_params = urlencode(options)
#             url = f"{self.base_url}{endpoint}?{query_params}"
#         else:
#             url = f"{self.base_url}{endpoint}"
#         data = self._get(url)
#         return data['value']

#     def get_schedule_ids(self, options=None):
#         """
#             Returns a list of dictionaries
#                 name -- schedule_id
#         """
#         process_schedules = self.get_all_schedules(options=options)
#         return [{schedule["Name"]: schedule["Id"] for schedule in process_schedules}]

#     def get_robot_ids(self, schedule_id=None, options=None):
#         endpoint = "/ProcessSchedules"
#         uipath_svc = f"/UiPath.Server.Configuration.OData.GetRobotIdsForSchedule(key = {schedule_id})"
#         if not schedule_id:
#             raise OrchestratorMissingParam(value="schedule_id", message="schedule id parameter is required")
#         if options:
#             query_params = urlencode(options)
#             url = f"{self.base_url}{endpoint}{uipath_svc}?{query_params}"
#         else:
#             url = f"{self.base_url}{endpoint}{uipath_svc}"
#         data = self._get(url)
#         return data['value']

#     def enable_process_schedule(self, enable: bool = False, schedule_ids=[]):
#         if not len(schedule_ids):
#             raise OrchestratorMissingParam(value="schedule_ids", message="At least un schedule id needs to be provided.")
#         else:
#             endpoint = "/ProcessSchedules"
#             uipath_svc = "/UiPath.Server.Configuration.OData.SetEnabled"
#             body = {
#                 "enabled": enable,
#                 "scheduleIds": schedule_ids
#             }
#             url = f"{self.base_url}{endpoint}{uipath_svc}"
#             return self._post(url, body=body)


# class Process(Orchestrator):
#     def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, session=None):
#         super().__init__(client_id=client_id, refresh_token=refresh_token, folder_id=folder_id)
#         if not tenant_name or not folder_id:
#             raise OrchestratorMissingParam(value="tenant_name, folder_id",
#                                            message="Required parameter(s) missing: tenant_name, folder_id")
#         self.tenant_name = tenant_name
#         self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
#         if session:
#             self.session = session
#         else:
#             self.session = requests.Session()

#     def get_all_processes(self, options=None):
#         """
#             Returns a list of all processes
#         """
#         endpoint = "/Processes"
#         if options:
#             query_params = urlencode(options)
#             url = f"{self.base_url}{endpoint}?{query_params}"
#         else:
#             url = f"{self.base_url}{endpoint}"

#         data = self._get(url)
#         return data['value']

#     def get_processes_key(self, options=None):
#         """
#             Returns a dictionary
#                 process title -- process key
#         """
#         processes = self.get_all_processes(options=options)
#         return [{process["Title"]: process["Key"]} for process in processes]

#     def download_process_package(self, process_key):
#         """
#             Doesnt work
#         """
#         endpoint = "/Processes"
#         uipath_svc = f"UiPath.Server.Configuration.OData.DownloadPackage(key='{process_key}')"
#         url = f"{self.base_url}{endpoint}{uipath_svc}"
#         return self._get(url)

#     def get_available_versions(self, process_key):
#         """
#         Gets all the available versions for a given process
#         """
#         endpoint = "/Processes"
#         uipath_svc = f"/UiPath.Server.Configuration.OData.GetProcessVersions(processId='{process_key}')"
#         url = f"{self.base_url}{endpoint}{uipath_svc}"
#         return self._get(url)

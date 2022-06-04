from datetime import datetime
import requests
import random
import json
import string
from pprint import pprint
import logging

from orchestrator.exceptions import OrchestratorAuthException, OrchestratorMissingParam


class OrchestratorHTTP(object):
    cloud_url = "https://cloud.uipath.com"
    account_url = "https://account.uipath.com"
    oauth_endpoint = "/oauth/token"
    _now = datetime.now()
    _token_expires = datetime.now()
    access_token = None

    def __init__(
        self,
        client_id=None,
        refresh_token=None,
        tenant_name=None,
        folder_id=None,
        session=None,
        file=None

    ):
        if not client_id or not refresh_token:
            if file:
                f = open(file)
                try:
                    data = json.load(f)
                    self.client_id = data["client_id"]
                    self.refresh_token = data["refresh_token"]
                    self.tenant_name = data["tenant_name"]
                    self.base_url = f"{self.cloud_url}/{self.tenant_name}/JTBOT/odata"
                    self.folder_id = data["folder_id"]
                except KeyError as err:
                    print(err)
                    raise
            else:
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
        self.expired = True

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
            r = self.session.post(url=url, data=json.dumps(body), headers=headers)
            token_data = r.json()
            token = token_data["access_token"]
            expiracy = token_data["expires_in"]
            self.access_token = token
            self._token_expires = expiracy
        except Exception as err:
            print(err)

    def _auth_header(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    @staticmethod
    def _content_header():
        return {"Content-Type": "application/json"}

    def _folder_header(self):
        if not self.folder_id:
            raise OrchestratorAuthException(value="folder id", message="folder cannot be null")
        return {"X-UIPATH-OrganizationUnitId": f"{self.folder_id}"}

    def _internal_call(self, method, endpoint, *args, **kwargs):
        # pprint(self.folder_id)
        # if self.expired:
        #     logging.debug("Token has expired")
        #     self._get_token()
        #     self.expired = False

        headers = self._auth_header()
        # pprint(headers)
        if method == "POST":
            headers.update(self._content_header())
        if self.folder_id:
            headers.update(self._folder_header())
        try:
            # print(endpoint)
            if kwargs:
                # pprint(kwargs)
                item_data = kwargs['body']['body']
                # pprint(json.dumps(item_data))
                # pprint(item_data)
                r = self.session.request(method, endpoint, json=item_data, headers=headers)
            else:
                r = self.session.request(method, endpoint, headers=headers)
                # print(r.status_code)
                if r.status_code == 401:
                    self._get_token()
                    headers = self._auth_header()
                    r_retry = self.session.request(method, endpoint, headers=headers)
                    return r_retry.json()
                if r.status_code not in range(200, 400):
                    logging.error(f"An error ocurred.\nStatus code: {r.status_code}")
                    # print(r.json())
            # print(endpoint)
            print(r.url)
            logging.debug(f"{r.status_code} ---- {r.url}")
            try:
                # pprint(r.json())
                return r.json()
            except requests.exceptions.JSONDecodeError:
                return r.text
        except Exception as err:
            print(err)
            raise

    def _get(self, url, *args, **kwargs):

        return self._internal_call("GET", url, args, kwargs)

    def _post(self, url, *args, **kwargs):
        # pprint(kwargs)
        return self._internal_call("POST", url, args, body=kwargs)

    def _put(self, url, *args, **kwargs):
        return self._internal_call("PUT", url, args, body=kwargs)

    def _delete(self, url, *args, **kwargs):
        return self._internal_call("DELETE", url, args, kwargs)

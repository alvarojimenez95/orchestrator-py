from datetime import datetime
import requests
import json


from orchestrator.exceptions import OrchestratorAuthException


class Orchestrator(object):
    """
    Base class from which the rest of the items, Robots, Folders,
    Assets will inherit. This class will containing the internal calls
    and the http methods, as well as the authentication method
    """

    cloud_url = "https://cloud.uipath.com"
    account_url = "https://account.uipath.com"
    oauth_endpoint = "/oauth/token"
    _token_expires = datetime.now()
    _access_token = None

    def __init__(
        self,
        client_id=None,
        refresh_token=None,
        tenant_name=None,
        folder_id=None,
        session=None,
    ):
        if not client_id or not refresh_token:
            raise OrchestratorAuthException(
                value=None, message="client id and refresh token cannot be left empty"
            )
        else:
            self.client_id = client_id
            self.refresh_token = refresh_token
            self.tenant_name = tenant_name
            self.folder_id = folder_id
            self.session = session

    def get_token(self):
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
            token = token_data["aceess_token"]
            expiracy = token_data["expires_in"]
            self._access_token = token
            self._token_expires = expiracy
        except Exception as err:
            print(err)

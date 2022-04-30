from orchestrator.orchestrator_http import OrchestratorHTTP
import requests
from orchestrator.exceptions import OrchestratorMissingParam

"""
    Asset class for dealing with Orchestrator requests which involve a given asset
"""


class Asset(OrchestratorHTTP):
    """
    Container class for asset entities in Orchestrator Cloud. 

    :param client_id - the client id of your cloud organization unit.
    :type client_id - str

    :param refresh_token - a refresh token. 
    :type refresh_token - str 

    :param tenant_name - your account's logical name
    :type tenant_name - str 

    :param folder_id - the id of the folder (UiPath's organizations unit)
    :type folder_id - str 

    :param folder_name - the name of the folder 
    :type folder_name : str 

    :param session - a session object to deal with the requests 
    :type session - Session 

    :param asset_id - the id of the asset 
    :type asset_id - int

    :param asset_name - the name of the asset
    :type asset_id - str 

    """

    def __init__(self, client_id, refresh_token, tenant_name, folder_id=None, folder_name=None, session=None, asset_id=None, asset_name=None):
        """Constructor"""
        super().__init__(client_id=client_id, refresh_token=refresh_token, tenant_name=tenant_name, folder_id=folder_id, session=session)
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

    def __str__(self):
        return f"Asset Id: {self.id} \nAsset Name: {self.name} \nFolder Id: {self.folder_id} \nFolder Name: {self.folder_name}"

    def info(self):
        """
        Gives back information about the current asset.
        """
        endpoint = f"/Assets({self.id})"
        url = f"{self.base_url}{endpoint}"
        return self._get(url)

    def edit(self, body=None):
        """
            Edits an asset 

            :param body - the body of the request with the attributes changed
            :type body - dict
        """
        endpoint = f"/Assets({self.id})"
        url = f"{self.base_url}{endpoint}"
        return self._put(url, body=body)

    def delete(self, body=None):
        endpoint = f"/Assets({self.id})"
        url = f"{self.base_url}{endpoint}"
        return self._delete(url, body=body)

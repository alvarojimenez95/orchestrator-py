![Tests](https://github.com/alvarojimenez95/orchestrator-py/actions/workflows/tests.yml/badge.svg)

# Python-Orchestrator

A library build to handle the [Orchestrator API](https://docs.uipath.com/orchestrator/reference/api-references)

## Quick Start

To initialize the class provide an instance of the `Orchestrator` object with the following credentials:

- `client_id`: your client id.
- `refresh_token`: a refresh token.
- `tenant_name`: your account logical name.

```py
from orchestrator import Orchestrator

client = Orchestrator(client_id = "CLIENT_ID",
                    refresh_token = "REFRESH_TOKEN",
                    tenant_name = "TENANT_NAME")
```

An optional parameter of a folder id can also be specified.

One can also initialize an instance by providing a route to a file containing the credentials in JSON format. For example, a file `dummy_credentials.json` in the parent directory with the structure

```json
{
  "client_id": "CLIENT_ID",
  "refresh_token": "REFRESH_TOKEN",
  "tenant_name": "TENANT_NAME",
  "folder_id": "FOLDER_ID"
}
```

can be used to initialize an instance by

```python
client = Orchestrator(file = "../dummy_credentials.json")
```

From an Orchestrator client, we can access different information about the folder, the queues, the assets of your cloud account. The following methods return properties of the folders of your Orchestrator account:

```py
# returns all the folders
folders = client.get_folders()

# returns a dictionary with the folder ids as keys and their names as values
dict_ids = client.get_folder_ids()

# returns a single folder by id
folder = client.get_folder_by_id(1263510)
```

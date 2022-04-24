from platform import machine
from orchestrator import Orchestrator

from dotenv import load_dotenv
import os
import time
from pprint import pprint

start = time.time()

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
TENANT_NAME = os.getenv('TENANT_NAME')
PRE_FOLDER_ID = os.getenv('PRE_FOLDER_ID')
MACHINE_IDENTIFIER = os.getenv('MACHINE_IDENTIFIER')

client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)

folder = client.get_folder_by_id(PRE_FOLDER_ID)

queue = folder.get_queue_by_id(110927)

item_content = {
    "Name": "Yo",
    "Apellido": "Test"
}

for i in range(0, 30):
    print("Empezando la transaccion")
    res = queue.start(machine_identifier=MACHINE_IDENTIFIER, specific_content=item_content)
    # pprint(res)
    time.sleep(2)
    item_id = res["Id"]
    print("Obteniendo el item")
    item = queue.get_item_by_id(item_id)
    time.sleep(2)
    print("Actualizando el status")
    item.set_transaction_status(success=True)
    # pprint(res2)


end = time.time()
print("Time taken: " + str(end - start))
# item = queue.get_queue_items()[0]
# print(item)
# item = queue.get_item_by_id(234609075)
# res = item.delete()
# pprint(res)

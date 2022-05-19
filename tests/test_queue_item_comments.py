import uuid
from orchestrator import Orchestrator
import logging
from dotenv import load_dotenv
import os
import aiohttp

import time
from pprint import pprint
logging.basicConfig(filename="test.log", filemode="w", level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')


start = time.time()

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
TENANT_NAME = os.getenv('TENANT_NAME')
PRE_FOLDER_ID = os.getenv('PRE_FOLDER_ID')
MACHINE_IDENTIFIER = os.getenv('MACHINE_IDENTIFIER')

client = Orchestrator(client_id=CLIENT_ID, refresh_token=REFRESH_TOKEN, tenant_name=TENANT_NAME)

folder = client.get_folder_by_id(int(PRE_FOLDER_ID))

queue = folder.get_queue_by_id(116803)


comments = queue.get_queue_item_comments()
pprint(comments)

end = time.time()
print("Time taken: " + str(end - start))
# item = queue.get_queue_items()[0]
# print(item)
# item = queue.get_item_by_id(234609075)
# res = item.delete()
# pprint(res)

import os
from orchestrator import Orchestrator
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
TENANT_NAME = os.getenv("TENANT_NAME")
PRE_FOLDER_ID = os.getenv("PRE_FOLDER_ID")
PROD_FOLDER_ID = os.getenv("PROD_FOLDER_ID")


def main():
    client = Orchestrator(
        client_id=CLIENT_ID,
        refresh_token=REFRESH_TOKEN,
        tenant_name=TENANT_NAME
    )

    process_schedules = client.get_folder_by_id(PROD_FOLDER_ID).get_process_schedules()
    for process in process_schedules:
        print(f"--------- ASSET: {process.name}---------")
        print(process)
        cron = process.schedule()
        print(f"Cron Expression: {cron}")


if __name__ == "__main__":
    main()

import os
import json
import time
import click
import requests
import numpy as np
from loguru import logger
from huggingface_hub import HfApi, SpaceHardware


FOLDER_TO_UPLOAD_PATH = "workers/"


def parse_credentials(credential_file):
    """Parse the credentials file containing the following info: HF_USER, HF_TOKEN, SERVER_ADDRESS, SERVER_PASSWORD
    """
    with open(credential_file, "r") as f:
        credentials = json.load(f)

    return credentials


@click.command(help="Dispatch the clients to the space")
@click.option("--credential-file", type=str, 
              help="""
Path to the credentials file (json format) containing the following info:
- HF_USER
- HF_TOKEN
- SERVER_ADDRESS
- SERVER_PASSWORD
""")
@click.option("--space", type=str, 
              help="Name of the space to be created")
@click.option("--nb-clients", type=int, default=1, 
              help="Number of clients to be created")
@click.option("--paid/--no-paid", type=bool, default=False, 
              help="Whether to use the paid version of the space")
def dispatch(credential_file, space, nb_clients, paid):
    """Dispatch the clients to the space
    """
    sp = SpaceHardware.CPU_UPGRADE if paid else SpaceHardware.CPU_BASIC
    credentials = parse_credentials(credential_file)
    user = credentials["HF_USER"]
    token = credentials["HF_TOKEN"]
    api = HfApi(token=token)

    for i in range(nb_clients):
        REPO_ID = f"{user}/{space}_{i}"
        logger.info(f"Dispatching client {REPO_ID}")

        res = api.create_repo(
            repo_id=REPO_ID, 
            private=True, 
            exist_ok=True, 
            repo_type="space", 
            space_sdk="docker",
            space_hardware=sp,
        )

        # adding secrets to the repo
        commons = dict(repo_id=REPO_ID, token=token)
        mem, nb_workers = ("16", "2") if sp == SpaceHardware.CPU_BASIC else ("8", "8")
        api.add_space_secret(**commons, key="MEM_PER_WORKERS", value=mem)
        api.add_space_secret(**commons, key="NB_WORKERS", value=nb_workers)
        api.add_space_secret(**commons, key="SERVER_ADDRESS", value=credentials["SERVER_ADDRESS"])
        api.add_space_secret(**commons, key="SERVER_PASSWORD", value=credentials["SERVER_PASSWORD"])
        api.add_space_secret(**commons, key="MANAGER_NAME", value=f"HF_Manager_{REPO_ID}")
        

        res = api.upload_folder(
            repo_id=REPO_ID, 
            repo_type="space", 
            folder_path=FOLDER_TO_UPLOAD_PATH)
        
        logger.info(f"Dispatched client {REPO_ID}")

        time.sleep(np.random.choice(np.arange(5, 35)))


        # while True:
        #     runtime = api.get_space_runtime(repo_id=REPO_ID)

        #     if runtime.stage.upper() == "RUNNING":
        #         response = requests.get(
        #             f"https://opendd-{SPACE_NAME}.hf.space/convert?input=C1=CC=C(C=C1)CC(C(=O)O)N",
        #             headers={"Authorization": f"Bearer {os.environ.get('HF_TOKEN')}"},
        #         )
        #         print(response.json())
        #         break
        #     else:
        #         print(f"{runtime.stage=}")
        #         print(f"{runtime.hardware=}")
        #         print(f"{runtime.requested_hardware=}")
        #         time.sleep(60) # 1 min


if __name__ == "__main__":
    dispatch()
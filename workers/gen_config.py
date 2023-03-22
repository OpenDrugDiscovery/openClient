import os

def template2config():
    """
        Replace the secrets in the template manager config
    """
    secrets = os.environ

    config_fname = "./manager.yml"
    with open(config_fname, "r") as fd:
        template = fd.read()
    
    config = template.format(MEM_PER_WORKERS=int(secrets["MEM_PER_WORKERS"]),
                             NB_WORKERS=int(secrets["NB_WORKERS"]),
                             SERVER_ADDRESS=secrets["SERVER_ADDRESS"],
                             SERVER_PASSWORD=secrets["SERVER_PASSWORD"])
    with open(config_fname, "w") as fd:
        fd.write(config)


if __name__ == "__main__":
    template2config()
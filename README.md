# QMODD CLIENT

## Install the shared environment of OpenDrugDiscovery

| :information_source: INFO                                                                                  |
|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Installing the environment will take time. If you check the `env.yml` file, you'll see it includes some very specific versions.  There's several issues on Github on improving the overall process. See e.g. [here](https://github.com/psi4/psi4/issues/2300) or [here](https://github.com/psi4/psi4/issues/2621). |

```bash
mamba create -n qmodd -f env.yml
mamba activate qmodd
```

## Usage
This repository offers the code to run QCFractal clients  on HuggingFace Spaces, Slurm supercomputers and personal computers. At the moment, only the first one is implemented

### Start QCFractal clients  on HuggingFace Spaces
Before running this script make sure that you are part of the OpenDrugDiscovery Organization on HuggingFace
```shell
# for more details on the options
python dispatch_hf.py --help

# to create 2 HF clients for computation 
python dispatch_hf.py --credentials-file /path/to/the/credential \
    --space test \
    --nb-clients 2 \
    --no-paid
```

Go to https://huggingface.co/{your_username} to see the spaces created. You can delete them if there is no job to run on the server side.

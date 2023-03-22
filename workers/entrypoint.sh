#!/bin/sh
set -e
pwd 

python3 gen_config.py

# sudo cp manager.yml /etc/qcfractal-manager/manager.yaml

qcfractal-manager  \
    --config-file manager.yml \
    --log-file-prefix /app/manager.log &

uvicorn main:app --host 0.0.0.0 --port 7860
#!/bin/bash

source envs_local.sh

function setup_db() {
  echo "Setting up DB for user ${1}"

  cd src/btwa_api \
    && alembic upgrade head \
    && python scripts.py add-user $1
}

if [ $# -ne 1 ]; then
  echo "Usage: ./setup_local.sh username"
  exit 1
fi

pip install -e .\
  && setup_db $1

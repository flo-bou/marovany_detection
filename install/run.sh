#!/bin/bash

# Get script folder location
# INSTALL_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
INSTALL_DIR=$(dirname "$(readlink -f "$0")")
cd $INSTALL_DIR

# run virtual env
source .venv/bin/activate

# run application
echo "Launching application"
python3 main.py

# shut down virtual env
echo "Application shut down"
deactivate

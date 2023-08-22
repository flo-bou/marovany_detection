#!/bin/bash

# TODO verify python version

# create virtual env
python3 -m venv .venv

# activate virtual env
source .venv/bin/activate

# verify pip availability
# python -m ensurepip --upgrade

# install dependancies
python3 -m pip install -r ./install/requirements.txt

# deactivate virtual env
deactivate

# make the run script usable from finder
chmod -v +x run_macos.command

# end message
echo ""
echo "Installation successful. You can now close this terminal."

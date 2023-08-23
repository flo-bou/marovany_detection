#!bin/bash

# TODO verify python version

# create virtual env
echo "Creating virtual environment..."
python3 -m venv .venv
echo "Virtual environment created."

# activate virtual env
source .venv/bin/activate

# verify pip availability
# python -m ensurepip --upgrade

# install dependancies
echo "Installing dependancies..."
python3 -m pip install -r ./install/requirements.txt
echo "Dependancies succefully installed."

# deactivate virtual env
deactivate

# make the run script usable from file explorer
cat run.sh > ../RUN_APP.sh
chmod -v +x ../RUN_APP.sh

# end message
echo ""
echo "Installation successful. You can now close this terminal."

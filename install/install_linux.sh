#!bin/bash

# check python environment
# sudo apt install python3-venv
# python3 -m ensurepip --upgrade
# sudo apt-get install libportaudio2 # required by sounddevice module

# create virtual env
echo "Creating virtual environment..."
python3 -m venv .venv
echo "Virtual environment created."

# activate virtual env
source .venv/bin/activate

# install dependancies
echo "Installing dependancies..."
python3 -m pip install -r ./install/requirements.txt
echo "Dependancies succefully installed."

# deactivate virtual env
deactivate

# make the run script usable from file explorer
cat install/run.sh > RUN_APP.sh
chmod +x RUN_APP.sh

# end message
echo ""
echo "Installation successful. You can now close this terminal."

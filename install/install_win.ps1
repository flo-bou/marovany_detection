
# check python environment
# python -m ensurepip --upgrade

# create virtual env
echo "Creating virtual environment..."
python -m venv .venv
echo "Virtual environment created."

# activate virtual env
. .venv\Scripts\activate

# install dependancies
echo "Installing dependancies..."
python -m pip install -r .\install\requirements.txt
echo "Dependancies succefully installed."

# deactivate virtual env
deactivate

# make the run script usable from file explorer
cat install/run_win.ps1 > RUN_APP.ps1
# chmod -v +x RUN_APP.sh

# end message
echo ""
echo "Installation successful. You can now close this PowerShell instance."

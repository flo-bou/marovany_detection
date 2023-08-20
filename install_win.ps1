# download source files
Invoke-WebRequest https://github.com/flo-bou/marovany_detection/archive/change-dependancies.zip -OutFile .\change-dependancies.zip

# set up folder
Expand-Archive .\change-dependancies.zip .\
Rename-Item .\marovany_detection-change-dependancies .\marovany_detection
Remove-Item .\change-dependancies.zip
cd .\marovany_detection

# TODO verify python version

# create virtual env
python -m venv .venv

# activate virtual env
. .venv\Scripts\activate

# verify pip availability
# python -m ensurepip --upgrade

# install dependancies
python -m pip install -r requirements.txt
echo "Installation successful."

# deactivate virtual env
deactivate

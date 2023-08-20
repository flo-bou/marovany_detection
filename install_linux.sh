# download source files
curl -LO https://github.com/flo-bou/marovany_detection/archive/change-dependancies.zip

# set up folder
unzip change-dependancies.zip
mv ./marovany_detection-change-dependancies ./marovany_detection
rm change-dependancies.zip
cd ./marovany_detection

# TODO verify python version

# create virtual env
python3 -m venv .venv

# activate virtual env
source .venv/bin/activate

# verify pip availability
# python -m ensurepip --upgrade

# install dependancies
python3 -m pip install -r requirements.txt
echo "Installation successful."

# deactivate virtual env
deactivate

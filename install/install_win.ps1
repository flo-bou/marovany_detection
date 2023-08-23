
# check python environment

# create virtual env
python -m venv .venv

# activate virtual env
. .venv\Scripts\activate

# verify pip availability
# python -m ensurepip --upgrade

# install dependancies
python -m pip install -r .\install\requirements.txt
echo "Installation successful."

# deactivate virtual env
deactivate

# end message
echo ""
echo "Installation successful. You can now close this terminal."

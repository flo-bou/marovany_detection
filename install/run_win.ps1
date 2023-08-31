
# run virtual env
. .\.venv\Scripts\activate

# run application
echo "Launching application"
python main.py

# shut down virtual env
echo "Application shut down"
deactivate

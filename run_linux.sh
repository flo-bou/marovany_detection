# run virtual env
source .venv/bin/activate

# run application
echo "Launching application"
python3 main.py

# shut down virtual env
echo "Application shut down"
deactivate

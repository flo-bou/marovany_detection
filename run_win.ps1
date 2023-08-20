# lancer l'environnment virtuel
. .\.venv\Scripts\activate

echo "Launching application"

# lancer l'application
python main.py

# à la fermeture désactiver l'environnement virtuel

echo "Application closed"

deactivate

# dl les sources sur github
Invoke-WebRequest https://github.com/flo-bou/marovany_detection/archive/change-dependancies.zip # -OutFile .\plinqo.zip
# écraser les fichiers
Expand-Archive .\change-dependancies.zip .\
# Rename-Item .\plinqo-main .\plinqo
Remove-Item .\change-dependancies.zip

# vérifier la version de python

# créer un environnement virtuel (vérifier que venv est présent)
python -m venv .venv

# python -m pip install --upgrade pip

# activer l'environnement virtuel
. .venv\Scripts\activate

# vérifier que pip est installé

# installer les dépendances (selon la version de python)
python -m pip install -r requirements.txt

deactivate

echo "Installation successful. You can now close that window."
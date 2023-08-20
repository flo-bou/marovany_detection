# Présentation
***marovany-detection*** est une application de bureau permettant de reconstituer au format midi des captations faites cordes à corde sur une marovany.

# Téléchargement
Les différentes versions compilées de l'application sont disponibles sur le dossier cloud suivant :
https://mega.nz/folder/hfUCmJDS#uPjSgocJ_ErcZ7DDEkvv0g

# Versions
## Windows
Pour lancer l’application, double-cliquez sur le fichier « marovany.exe ».
Elle a été réalisée sous Windows 10 et ne fonctionnera probablement pas sous les versions plus anciennes de Windows.
Il est possible que votre antivirus empêche le lancement de l'application. Dans ce cas, il est nécessaire d'autoriser le lancement du fichier « marovany.exe » ou de
suspendre l'antivirus.

## MacOS
Pour lancer l’application, ouvrez (cmd + O) le fichier « marovany ».
Elle a été réalisée sous macOS 10.15 et ne fonctionnera probablement pas sous les versions plus anciennes de macOS.

## Linux
Pour lancer l’application, double-cliquez sur le fichier « marovany ».
La version 0.2 a été réalisée sous Ubuntu 22 et ne devrait être compatible qu'avec des versions récentes de Linux.

# Installation

Install dependancies :
```sh
pip install -r requirements.txt
```

# Fonctionnement

Run dev environmement :
```sh
source .env/Scripts/activate
python -m flask run --debug
```

## Importer des fichiers
Une fois l’application lancée, il faut y importer des fichiers wav captés sur la marovany.
Pour cela, utilisez le menu « File » puis sélectionnez l’une des options suivante :
* « import a directory » : vous sélectionnez un dossier (et uniquement un dossier) qui contient directement des fichiers .wav. L’application va reconnaître les fichiers wav et proposer un widget d’analyse pour chacun de ces fichiers.
* « import a single file » : vous permet d’ajouter un unique fichier .wav. L’application va ajouter un widget d’analyse correspondant à ce fichier.

## Reconnaissance automatique des cordes
L’application permet de reconnaître les notes des cordes d’après leur noms de fichier. Pour tirer profit de cette fonctionnalité, il suffit de mettre le nom de la note/corde dans le nom du fichier associé.
Les noms de note reconnus sont de la forme : « B#3, G2, E0, Cb4 … ». Par exemple un fichier nommé « 15_D3_140789_345.wav » sera reconnu en tant que corde D3

## Paramètres
***Note name*** : Nom de la note/corde. Doit être de la forme « B#3, G2, E0, Cb4 … »

***Duration of analysis*** : Durée de l’analyse en secondes, à partir du début du fichier. Une valeur de 60 va proposer une analyse des 60 premières secondes du fichier.

***Filter timescale*** : paramètre utilisé pour la segmentation de note : longueur du filtre médian. Plus cette valeur est grande plus l’enveloppe du signal est lissée. La valeur par défaut est de 80.

***Threshold*** : paramètre utilisé pour la détection de note : niveau d’énergie au-dessus duquel l’occurrence d’une note est détectée. Le plus cette valeur est grande, le moins d’événements/vibrations seront considérés comme des notes jouées. Ce paramètre est visible sous la forme d’une ligne horizontale en pointillée sur la figure de *note tracking*. La valeur par défaut est de 0.15.

***Minimum note duration*** : paramètre pour la segmentation de note : durée minimale en seconde sous laquelle un événement/une note n’est pas prise en compte. La valeur par défaut est de 0.03.

# Licence
[ISC](https://www.isc.org/licenses/)

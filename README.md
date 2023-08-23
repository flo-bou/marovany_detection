# Présentation

***marovany-detection*** est une application de bureau permettant de reconstituer au format midi des captations faites cordes à corde sur une marovany.

# Install

1. To fetch the source files, go to the [Github page](https://github.com/flo-bou/marovany_detection) and push the green button named "Code" then "Download Zip".
2. Put the zip file wherever you want to install the app. Unzip.
3. Open the terminal (Launchpad > search "Terminal" on macOS)
4. In the terminal, go inside the folder you just unziped.
5. Run the installation script according to you OS:
    * for macOS, type <code>source install/install_macos.sh</code>
    * for Linux, type <code>source install/install_linux.sh</code>
    * for Windows, type <code>. install\install_win.ps1</code>
6. Wait for installation to complete.
7. That's it. You can now run the application.

# Run

To run the application :
* on macOS, double-clic on the <code>RUN_APP.command</code> file 
* on Linux, double-clic on the <code>RUN_APP.sh</code> file 
* on Windows, double-clic on the <code>RUN_APP.ps1</code> file 

# Fonctionnement

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

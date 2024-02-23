# from sys import argv, exit
import json
# from urllib.parse import unquote

from flask import Flask, render_template, send_file, request

from utils import *

app = Flask(__name__)

@app.get("/")
def send_index_page():
    return render_template('index.html')


@app.get("/file")
def send_audio_file():
    """ Send audio file located at 'fpath'
    
    URL query params:
        fpath: string 
            Full path of the audio file to send.
            
    Returns: 
        The requested file.
    """
    fpath: str = request.args.get("fpath")
    return send_file(fpath)


@app.get("/files_list")
def send_files_list():
    """Send list of .wav files' name located in 'location' directory.
    
    URL query params:
        location: string
            Directory path.
            
    Returns: str
        Json string containing list of files' name.
    """
    wav_files: dict = get_wav_files_locations(request.args.get("location"))
    return json.dumps(wav_files)


@app.get("/file_notes")
def send_file_notes():
    """Send json data related to file located at 'fpath'.
    
    URL query params:
        fpath: str
            Full path of the file.
    
    Returns: str
        Data about the targeted file as a json string.
    """
    data: str = get_notes(request.args.get("fpath"))
    return data


@app.post("/file_notes")
def save_file_notes():
    """Receives data about an audio file and stores it.
    
    Data is received from a POST request as a json string.
    
    Returns: str
        Indicator of succes of the storing.
        'ok' if data was stored.
        'ko' if data was not stored.
    """
    data: dict = request.json
    result: str = save_notes(data)
    return result


@app.get("/old")
def index_old():
    return render_template('index.old.html')


@app.get("/test")
def say_hello():
    return "Hello from the server"


# préparer une fermeture de l'app (quand on ferme le shell ?)

# Start with flask web app, with debug as True,
# only if this is the starting page
# if(__name__ == "__app__"):
#     app.run(debug=True)

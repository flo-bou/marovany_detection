# from sys import argv, exit
import json
# from urllib.parse import unquote

from flask import Flask, render_template, send_file, request

from utils import *

app = Flask(__name__)

@app.get("/")
def index():
    return render_template('index.html')

@app.get("/old")
def index_old():
    return render_template('index.old.html')


@app.get("/test")
def say_hello():
    return "Hello from the server"


@app.get("/file")
def send_audio_file():
    args = request.args
    print("request.args : ")
    print(request.args)
    return send_file(args.get("fpath"))


@app.get("/files_list")
def send_files_list():
    args = request.args
    wav_files = get_wav_files_locations(args.get("location"))
    return json.dumps(wav_files)



# préparer une fermeture de l'app (quand on ferme le shell ?)

# Start with flask web app, with debug as True,
# only if this is the starting page
# if(__name__ == "__app__"):
#     app.run(debug=True)

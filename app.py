from sys import argv, exit
from time import time

from flask import Flask, render_template, send_file

# from MainWindow import MainWindow

app = Flask(__name__)

@app.get("/")
def index():
    return render_template('index.html')

@app.post("/")
def send_fig():
    return "Hello"

@app.get("/file")
def send_audo_file():
    return send_file("C:/Users/admin/Project/marovany/capteurs/17-D5-140709_1628.wav")


# préparer une fermeture de l'app (quand on ferme le shell ?)

# old app :  MainWindow() , mainWindow.show()


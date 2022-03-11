# mongon_api.py
# This program is supposed to set up an api to communicate with stream elements
# This api needs to communicate with 'mongon_chat_history.csv'
# inspired by https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
# imports
import flask
from flask import request
import pandas as pd
import threading
import sys
import os
import time


# link: http://127.0.0.1:5000/

app = flask.Flask(__name__)
app.config["DEBUG"] = True


path = r"C:\Users\socra\Documents\git-hut_stuff\twitch_interaction_sesaw_project\Twitch_Integration_Project\mongon_chat_history.csv"
escaper = None

def escape_route():
    global escaper
    while escaper != "Y":
        escaper = str(input("Exit now? Enter \'Y\': \n")).strip()
    os._exit(os.X_OK)


def amogusfinder():
    variants = ["amogus", "among us", "amog us"]

    @app.route('/amogus', methods=['GET'])
    def amogusget():
        dfchat = pd.read_csv(path)
        if 'name' in request.args:
            name = str(request.args['name'])
        else:
            return "{no name!}"
        try:
            dfusername = dfchat[(dfchat["username"] == name)]
            dfstring = dfusername[dfusername["message"].str.contains('|'.join(variants), 
                na=False, case=False, regex=True)]
            return str(dfstring["message"].count())
        except:
            return "{ERROR Mongon FUCKED UP HIS PROGRAM (failed look-up)}"


def susfinder():
    variants = ["sus"]

    @app.route('/sus', methods=['GET'])
    def susget():
        dfchat = pd.read_csv(path)
        if 'name' in request.args:
            name = str(request.args['name'])
        else:
            return "{no name!}"
        try:
            dfusername = dfchat[(dfchat["username"] == name)]
            dfstring = dfusername[dfusername["message"].str.contains('|'.join(variants), 
                na=False, case=False, regex=True)]
            return str(dfstring["message"].count())
        except Exception as e:
            return f"ERROR Mongon FUCKED UP HIS PROGRAM (failed look-up)"


def bakafinder():
    variants = ["baka"]
    @app.route('/baka', methods=['GET'])
    def bakaget():
        dfchat = pd.read_csv(path)
        if 'name' in request.args:
            name = str(request.args['name'])
        else:
            return "{no name!}"
        try:
            dfusername = dfchat[(dfchat["username"] == name)]
            dfstring = dfusername[dfusername["message"].str.contains('|'.join(variants), 
                na=False, case=False, regex=True)]
            return str(dfstring["message"].count())
        except:
            return "{ERROR Mongon FUCKED UP HIS PROGRAM (failed look-up)}"


def wordfinder():
    @app.route('/word', methods=['GET'])
    def wordget():
        dfchat = pd.read_csv(path)

        if 'name' in request.args:
            name = str(request.args['name'])
        else:
            return "{no name!}"

        if 'word' in request.args:
            word = str(request.args['word'])
        else:
            return "{no word!}"
            
        try:
            dfusername = dfchat[(dfchat["username"] == name)]
            dfstring = dfusername[dfusername["message"].str.contains(word, 
                na=False, case=False, regex=True)]
            return str(dfstring["message"].count())
        except:
            return "{ERROR Mongon FUCKED UP HIS PROGRAM (failed look-up)}"


def main():
    global dfchat
    # escape_route_thread = threading.Thread(target = escape_route)
    # escape_route_thread.start()
    amogusfinder()
    susfinder()
    bakafinder()
    wordfinder()
    app.run()


main()


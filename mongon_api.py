# mongon_api.py
# This program is supposed to set up an api to communicate with stream elements
# This api needs to communicate with 'mongon_chat_history.csv'
# This build only lanches a local API with http://127.0.0.1:5000/
# This program only mimics the server API (path definition is different)
# imports
import flask
from flask import request
import pandas as pd
import threading
import sys
import os
import csv
import ast


# api initialization using flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# csv file and gobal variables initialiation
path = r"C:\Users\socra\Documents\git-hut_stuff\twitch_interaction_sesaw_project\Twitch_Integration_Project\mongon_chat_history.csv"
escaper = None
header = ['dt', 'channel', 'username', 'message']


# created escape loop for debugging
def escape_route():
    global escaper
    while escaper != "Y":
        escaper = str(input("Exit now? Enter \'Y\': \n")).strip()
    os._exit(os.X_OK)


# api GET routes created for stream 

def commands():
    
    @app.route('/commands', methods=['GET'])
    def commandget():
        return '''Mongon's custom commands: 
        !wordcount [username] [word], !amoguscount [username].
'''


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
        except Exception:
            return "ERROR Mongon FUCKED UP HIS PROGRAM (failed look-up)"


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


# api POST routes designed to receive chat messages from twitch_cat_receiver.py

def update_online_csv():
    @app.route('/respdict', methods=['POST'])
    def wordreceive(): 

        # converting binary stringb back to dict
        d = request.get_data()
        d = d.decode("UTF-8")
        d = ast.literal_eval(d)

        # writing to server's csv file
        with open(path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames = header)
            writer.writerow(d) 

        return d


# main method. could not define it at beginnig of file because of @app.route commands
def main():
    # escape_route_thread = threading.Thread(target = escape_route)
    # escape_route_thread.start()

    # get requests
    commands()
    amogusfinder()
    susfinder()
    bakafinder()
    wordfinder()

    # post requests
    update_online_csv()

    # starting api
    if __name__ == '__main__':
        app.run()


main()

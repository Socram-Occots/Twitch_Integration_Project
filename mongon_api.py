# mongon_api.py
# This program is supposed to set up an api to communicate with stream elements
# This api needs to communicate with 'mongon_chat_history.csv'
# inspired by https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
# imports
import flask
from flask import request, jsonify
import pandas as pd

# link: http://127.0.0.1:5000/

app = flask.Flask(__name__)
app.config["DEBUG"] = True

path = r"C:\Users\socra\OneDrive\Documents\College\twitch-integration-project\Twitch_Integration_Project\mongon_chat_history.csv"

def retrieve_database():
    return pd.read_csv(path)


def amogusfinder():
    dfchat = retrieve_database()
    variants = ["amogus", "among us", "amog us"]

    @app.route('/amogus', methods=['GET'])
    def amogusget():
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
    dfchat = retrieve_database()
    variants = ["sus", "sussy", "susy", "$u$"]

    @app.route('/sus', methods=['GET'])
    def susget():
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


def bakafinder():
    dfchat = retrieve_database()
    variants = ["baka", "b4k4"]

    @app.route('/baka', methods=['GET'])
    def bakaget():
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


def main():
    amogusfinder()
    susfinder()
    bakafinder()
    app.run()


main()


# unused
'''
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]
'''

'''
@app.route('/', methods=['GET'])
def home():
    return ''''''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>''''''
'''
'''
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)
'''
'''
@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)
'''


'''
def countingString(dfstring, variants):
    count = 0
    for subStr in variants:
        if subStr in dfstring:
            count += 1
    return count
'''


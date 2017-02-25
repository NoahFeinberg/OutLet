from flask import Flask
from flask import render_template
app = Flask(__name__)

app.debug = 'true'

dictionaryArray = [{'title': 'Test 1', 'source': 'Source 1'}, {'title': 'Test 2', 'source': 'Source 2'}]

@app.route('/')
def hello_world():

    return render_template('index.html', searchresults=dictionaryArray)


if __name__ == '__main__':
    app.run()

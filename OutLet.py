from flask import Flask
from flask import render_template
import power
app = Flask(__name__)

app.debug = 'true'

dictionaryArray = [{'title': 'Test 1', 'source': 'Source 1'}, {'title': 'Test 2', 'source': 'Source 2'}]

@app.route('/')
def first_page():

    return render_template('index.html')

@app.route('/list')
def list_page():

    return render_template('index.html', )


if __name__ == '__main__':
    app.run()
    power.makeReq('iraq', '2e75b4df-809f-4f48-904d-dfd4c2615f60')

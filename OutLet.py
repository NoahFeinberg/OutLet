from flask import Flask
from flask import render_template
from flask import request
import power
app = Flask(__name__)

app.debug = 'true'

dictionaryArray = [{'title': 'Test 1', 'source': 'Source 1'}, {'title': 'Test 2', 'source': 'Source 2'}]

dataSet = []


@app.route('/')
def first_page():

    return render_template('index.html')

"""
@app.route('/list', methods=['POST', 'GET'])
def list_page():
    global dataSet
    dataSet = []

    if request.method == 'POST':
        html_data = request.form['searchBar']
        for site in html_data:
            dataSet.append(dict('body': )
            initialSentiment.append(power.analyze(site[0]))
            modifiedData.append(power.modifyNews(site[0]))
        for site in modifiedData:
            finalSentiment.append(power.analyze(site))
    return render_template('index.html')

"""


@app.route('/viewArticle', methods=['POST', 'GET'])
def view_article():
    if request.method == 'POST':
        article = request.form['searchBar']
        initialSentiment = power.analyze(article)
        modifiedArticle = power.modifyNews(article)
        finalSentiment = power.analyze(modifiedArticle)
        """
        article_body = request.form['article_body']
        article_new_body = request.form['article_new_body']
        """
    return render_template('index.html', article=article, initSent=initialSentiment.sentiment, newbody=modifiedArticle, finalSentiment=finalSentiment.sentiment)


if __name__ == '__main__':
    app.run()

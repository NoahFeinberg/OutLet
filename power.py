import requests
import urllib, os, csv
from HTMLParser import HTMLParser
import html2text, unirest
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import cPickle as pickle
import nltk
import pickle
from watson_developer_cloud import AlchemyLanguageV1, ToneAnalyzerV3
import json
from nltk import tokenize
from PyDictionary import PyDictionary


class TitleParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.match = False
        self.title = ''

    def handle_starttag(self, tag, attributes):
        self.match = True if tag == 'title' else False

    def handle_data(self, data):
        if self.match:
            self.title = data
            self.match = False


#def makeReq(text_string):

    """
    url = 'https://acceleratedmobilepageurl.googleapis.com/v1/ampUrls:batchGet'

    resp = unirest.post("https://webhose.io/search", headers={"Accept": "application/json"},
            params={"q": query, "thread.country": "United States",
                    "site_type": "news", "domain_rank": '<=2500',
                    "token": token,
                    "size": 2
                    })

    amp_request = resp.raw_body
    print(amp_request)
    parser = TitleParser()

    for ampUrl in amp_request['ampUrls']:
        response = urllib.urlopen(ampUrl['cdnAmpUrl'])
        html = str(response.read())
        html = html.decode('ascii', errors='ignore')
        parser.feed(html)
        title = parser.title
        html = html2text.html2text(html)

    if 'urlErrors' in amp_request:
        for normalUrl in amp_request['urlErrors']:
            response = urllib.urlopen(normalUrl['originalUrl'])
            html = str(response.read())
            html = html.decode('ascii', errors='ignore')
            parser.feed(html)
            title = parser.title

    return zip(html,title)
    """
def analyze(query):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "trained_classifier.pickle")
    cl = pickle.load(open(json_url))
    query = query.decode('ascii', errors="ignore")
    output = TextBlob(query, classifier=cl, analyzer=NaiveBayesAnalyzer())

    return output

def modifyNews(textData):
    # Initialize the dictionary
    dictionary = PyDictionary()

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "config.json")
    json_watson_config = json.load(open(json_url))

    # Use the pickle file if you do not want to retrain the object
    tnt_url = os.path.join(SITE_ROOT, "tnt_brown_pos_tagger.pickle")
    tnt_pos_tagger = pickle.load(open(tnt_url))
    query = textData.decode('ascii', errors="ignore")
    alchemy_language = AlchemyLanguageV1(api_key=json_watson_config['Alchemy_API_Key'])
    entities_alchemy = alchemy_language.combined(
        text=query.decode('ascii', errors="ignore"),
        extract='entities,keywords',
        sentiment=1,
        max_items=1)
    entity_list = []
    for entity in entities_alchemy['entities']:
        entity_list.append(entity['text'])

    tone_analyzer = ToneAnalyzerV3(
        username=json_watson_config['TONE_ANALYZER']['user'],
        password=json_watson_config['TONE_ANALYZER']['password'],
        version='2016-05-19')

    json_watson_config.close()

    sentences = tokenize.sent_tokenize(query.decode('ascii', errors="ignore"))

    newParagraph = ""
    range_ext = 0
    for sentence in sentences:
        tagged_sent = tnt_pos_tagger.tag(nltk.word_tokenize(sentence))
        if any(ext in sentence for ext in entity_list) or range_ext > 0:
            range_ext += 2
            for i in xrange(0, len(tagged_sent)):
                if "JJ" in tagged_sent[i][1] or "RB" in tagged_sent[i][1] or "VB" in tagged_sent[i][1]:
                    syn_list = [tagged_sent[i][0]]
                    syn_list += dictionary.synonym((tagged_sent[i][0]))
                    joy_index = 0
                    syn_index = 0
                    for j in xrange(0, len(syn_list)):
                        tone_json = tone_analyzer.tone(text=syn_list[j])
                        if joy_index < tone_json['document_tone']['tone_categories'][0]['tones'][4]['score']:
                            joy_index = tone_json['document_tone']['tone_categories'][0]['tones'][4]['score']
                            syn_index = j
                    tagged_sent[i] = (syn_list[syn_index], tagged_sent[i][1])
        for ind_tag in tagged_sent:
            newParagraph += str(ind_tag[0])
            newParagraph += ' '
        if range_ext > 0:
            range_ext -= 1

    return newParagraph


def txttocsv():

    dcount = 0
    rcount = 0

    with open('train.csv', 'w') as csvfile:
        for i in os.listdir(os.getcwd() + '/training_set'):
            if (rcount + dcount) < 500:
                if 'D' in i and dcount < 250:
                    party = 'pos'
                    dcount += 1
                elif rcount < 250:
                    party = 'neg'
                    rcount += 1

                segment = open('training_set/' + i, 'rb')
                segment = ''.join(segment.readlines()).replace('\n', '')

                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([segment, party])

            else:

                break

    return

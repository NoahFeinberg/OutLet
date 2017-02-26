import requests
import urllib.request
from html.parser import HTMLParser

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

url = 'https://acceleratedmobilepageurl.googleapis.com/v1/ampUrls:batchGet'

orig_urls = ['http://www.breitbart.com/big-journalism/2015/09/26/washington-post-confirms-hillary-clinton-started-the-birther-movement/',
             'https://www.theguardian.com/membership/2016/feb/24/todays-release-of-accelerated-mobile-pages-amp',
             'http://bit.ly/28lya4p']

api_key = input('Api key: ')
data = dict(key=api_key, urls=orig_urls)

r = requests.post(url, data=data, allow_redirects=True)
amp_request = r.json()
print(amp_request)
parser = TitleParser()

for ampUrl in amp_request['ampUrls']:
    response = urllib.request.urlopen(ampUrl['cdnAmpUrl'])
    html = str(response.read())
    parser.feed(html)
    title = parser.title
    print(title)
    print(html)

if 'urlErrors' in amp_request:
    for normalUrl in amp_request['urlErrors']:
        response = urllib.request.urlopen(normalUrl['originalUrl'])
        html = str(response.read())
        parser.feed(html)
        title = parser.title
        print(title)
        print(html)



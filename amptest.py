import requests
import urllib
from HTMLParser import HTMLParser
import html2text, unirest


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

orig_urls = ['http://www.dw.com/en/us-democrats-pick-tom-perez-as-new-chairman/a-37718486',
             'https://www.theguardian.com/membership/2016/feb/24/todays-release-of-accelerated-mobile-pages-amp',
             'http://bit.ly/28lya4p']


def makeReq(query, token):
    resp = unirest.post("https://webhose.io/search", headers={"Accept": "application/json"},
                            params={"q": query, "thread.country": "United States",
                                    "site_type": "news", "domain_rank": '<=2500',
                                    "token": token,
                                    "size": 2
                                    })

    print resp.code  # The HTTP status code
    print resp.headers  # The HTTP headers
    print resp.body  # The parsed response
    print resp.raw_body  # The unparsed response

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
        #print(title)
        print(html)

    if 'urlErrors' in amp_request:
        for normalUrl in amp_request['urlErrors']:
            response = urllib.urlopen(normalUrl['originalUrl'])
            html = str(response.read())
            html = html.decode('ascii', errors='ignore')
            parser.feed(html)
            title = parser.title
            print(title)
            print(html)


makeReq('tesla', '2e75b4df-809f-4f48-904d-dfd4c2615f60')
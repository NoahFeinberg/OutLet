import requests

url = 'https://acceleratedmobilepageurl.googleapis.com/v1/ampUrls:batchGet'

orig_urls = ['http://www.breitbart.com/big-journalism/2015/09/26/washington-post-confirms-hillary-clinton-started-the-birther-movement/',
             'https://www.example.org/article-without-amp-version',
             'https://www.theguardian.com/membership/2016/feb/24/todays-release-of-accelerated-mobile-pages-amp',
             'http://bit.ly/28lya4p']

api_key = input('Api key: ')
data = dict(key=api_key, urls=orig_urls)

r = requests.post(url, data=data, allow_redirects=True)
print(r.json())

import urllib.parse
import urllib.request
import base64
import json

import api_keys

# Generate an authcode for the twitter API.
def get_authcode():
    key = urllib.parse.quote_plus(api_keys.twitter_key)
    secret = urllib.parse.quote_plus(api_keys.twitter_secret)
    cred = base64.b64encode("{}:{}".format(key, secret).encode('utf-8'))

    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', 'Basic {}'.format(cred.decode('utf-8')))]

    data = urllib.parse.urlencode({'grant_type': 'client_credentials'})
    data = data.encode('ascii')

    with opener.open('https://api.twitter.com/oauth2/token', data) as f:
        j = json.load(f)
        return j["access_token"]

# Returns a list of tweets on each day of
def find_tweets(q):
    authcode = get_authcode()

    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', 'Bearer {}'.format(authcode))]

    query = urllib.parse.urlencode({
        'q': q,
        'result_type': 'popular', # popular, mixed, recent
        'count': 30, # Max 100
    })

    with opener.open('https://api.twitter.com/1.1/search/tweets.json?{}'.format(query)) as f:
        return json.load(f)

import urllib.error
try:
    print(find_tweets('TWTR'))
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.read())

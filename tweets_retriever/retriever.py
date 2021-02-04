import requests
import json
import re

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from . import key

BEARER_TOKEN = key.BEARER_TOKEN

def get_query(username, query):
    if username == ['']:
        user_query = user_query = [('{}'.format(query)) for user in username]
    else:
        user_query = [('from:{} {}'.format(user, query)) for user in username]
    return user_query

def create_url(query, fields="author_id"):
    tweet_fields = 'tweet.fields={}'.format(fields)
    api_url = [('https://api.twitter.com/2/tweets/search/recent?query={}&{}'.format(q,tweet_fields)) for q in query]
    print (api_url)
    return api_url

def get_tweets(api_url):
    headers = {"Authorization": "Bearer {}".format(BEARER_TOKEN), "Content-Type": "application/json"}
    tweet_id = []
    response = requests.request("GET", api_url, headers=headers)
    publisher = re.findall(r"\w+", api_url)[10]
    tweets_json = json.dumps(response.json())
    tweets = json.loads(tweets_json)
    try:
        for tweet in tweets['data']:
            tweet_id.append({'id':tweet['id'], 'publisher':publisher})
    except:
        print('No tweets from ' + publisher)
    return tweet_id

def get_tweet_html(tweet_id):
    headers = {"Authorization": "Bearer {}".format(
        BEARER_TOKEN), "Content-Type": "application/json"}
    url = 'https://publish.twitter.com/oembed?url=https://twitter.com/{}/status/{}'.format(
        tweet_id['publisher'], tweet_id['id'])
    response = requests.request("GET", url, headers=headers)
    embed_tweet_json = json.dumps(response.json())
    embed_tweet = json.loads(embed_tweet_json)
    html = {'html': embed_tweet['html']}
    return html

def get_embedded_tweets(api_url):
    with ThreadPoolExecutor() as executor:
        tweets_id = list(executor.map(get_tweets, api_url))
        embedded_tweets = []
        for tweet in tweets_id:
            html = list(executor.map(get_tweet_html,tweet))
            for x in html:
                embedded_tweets.append(x)
    return embedded_tweets
    
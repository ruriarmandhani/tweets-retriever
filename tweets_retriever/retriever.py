import requests
import json
import re
from datetime import datetime

def get_query(username, query):
    user_query = [('from:{} {}'.format(user, query)) for user in username]

    # print(user_query)
    return user_query


def create_url(query, fields="author_id"):
    # start_date = datetime.utcnow().strftime('%Y-%m-%dT00:00:00Z')
    # end_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00Z')
    
    tweet_fields = 'tweet.fields={}'.format(fields)

    # api_url = [ ('https://api.twitter.com/2/tweets/search/recent?query={}&{}&start_time={}&end_time={}'.format(q, tweet_fields, start_date, end_date)) for q in query]
    api_url = [ ('https://api.twitter.com/2/tweets/search/recent?query={}&{}'.format(q, tweet_fields)) for q in query]

    # print (api_url)
    return api_url


def get_tweets(bearer_token, api_url):
    headers = {"Authorization": "Bearer {}".format(
        bearer_token), "Content-Type": "application/json"}

    tweet_id = []
    for url in api_url:
        response = requests.request("GET", url, headers=headers)

        tweets_json = json.dumps(response.json())

        tweets = json.loads(tweets_json)

        publisher = re.findall(r"\w+", url)[10]

        try:
            for tweet in tweets['data']:
                tweet_id.append({'id':tweet['id'], 'publisher':publisher})
        except:
            print('No tweets from ' + publisher)
    # print(tweet_id)
    return tweet_id

def embed_tweets(tweet_id, bearer_token):
    link = []

    headers = {"Authorization": "Bearer {}".format(
        bearer_token), "Content-Type": "application/json"}

    for id in tweet_id:
        url = 'https://publish.twitter.com/oembed?url=https://twitter.com/{}/status/{}'.format(id['publisher'],id['id'])
        response = requests.request("GET", url, headers=headers)
        embed_tweet_json = json.dumps(response.json())
        embed_tweet = json.loads(embed_tweet_json)
        link.append({'link':embed_tweet['html']})

    # print(link)
    return link


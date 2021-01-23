import requests
import json
import re
from datetime import datetime

def get_query(username, query):
    # user_query = []

    user_query = [('from:{} {}'.format(user, query)) for user in username]

    # for user in username:
    #     user_query.append('from:{} {}'.format(user, query))

    # print(user_query)
    return user_query


def create_url(query, fields="author_id"):
    # api_url = []
    start_date = datetime.utcnow().strftime('%Y-%m-%dT00:00:00Z')
    end_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:00Z')
    
    tweet_fields = 'tweet.fields={}'.format(fields)

    api_url = [ ('https://api.twitter.com/2/tweets/search/recent?query={}&{}&start_time={}&end_time={}'.format(q, tweet_fields, start_date, end_date)) for q in query]

    # for q in query:
    #     api_url.append(
    #         'https://api.twitter.com/2/tweets/search/recent?query={}&{}&start_time={}&end_time={}'.format(q, tweet_fields, start_date, end_date))

    # print (api_url)
    return api_url


def get_tweets(bearer_token, api_url):
    headers = {"Authorization": "Bearer {}".format(
        bearer_token), "Content-Type": "application/json"}

    # data_list =[]
    tweet_id = []
    for url in api_url:
        response = requests.request("GET", url, headers=headers)
        # if response.status_code != 200:
        #     raise Exception(response.status_code, response.text)

        tweets_json = json.dumps(response.json())

        tweets = json.loads(tweets_json)

        try:
            for tweet in tweets['data']:
                tweet_id.append({'id':tweet['id'], 'publisher':re.findall(r"\w+", url)[10]})
        except:
            print('no tweets')
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
# Searches 100 most recent tweets on Twitter. The input performs search exactly as it would on the front end.
# Queries can use filters (e.g. "flight :(" returns tweets with a negative attitude containing "flight")")
# All filters/search operators w/ examples listed here: https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/guides/standard-operators")

from requests_oauthlib import OAuth1
import authentication
import json
import re
import requests
import urllib.parse
from flask import request
import authentication

def oauth(r):
    r.headers["Authorization"] = authentication.bearer_token
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r

def search_tweets(keywords):
    search_query = keywords.strip()
    search_query = re.sub(r"\W+", "", search_query) # only alphanumeric
    search_query = urllib.parse.quote(search_query)

    query_tweet_fields = 'created_at'
    query_user_fields = 'username,profile_image_url,location'

    url = "https://api.twitter.com/2/tweets/search/recent?query=" + search_query + "&expansions=author_id&tweet.fields=" + query_tweet_fields + "&user.fields=" + query_user_fields

    raw_json_tweets = requests.request("GET", url, auth=oauth).json()

    tweets = {}
    for i in range(len(raw_json_tweets['data'])):
        for j in range(len(raw_json_tweets['includes']['users'])):
            print('Posted: ' + raw_json_tweets['data'][j]['created_at'])
            print('Username: ', raw_json_tweets['includes']['users'][j]['username'])
            print('Tweet: ', raw_json_tweets['data'][j]['text'])
            print('\n')

if __name__ == "__main__":
    keywords = input("\nEnter: ")
    search_tweets(keywords)

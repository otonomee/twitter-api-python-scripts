import json
import requests
import itertools
from requests_oauthlib import OAuth1
import myauth

access_token = myauth.access_token
access_secret = myauth.access_secret
consumer_key = myauth.consumer_key
consumer_secret = myauth.consumer_secret
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
screen_name = myauth.screen_name

# returns list of followers user ids
def get_follower_users():
    follower_user_ids = {}
    follower_paginate_id = 0
    follower_json_list_index = 0
    get_follower_users = "https://api.twitter.com/1.1/followers/ids.json?cursor=-1&screen_name=" + screen_name + "&count=5000"
    follower_user_ids = json.loads(requests.get(get_follower_users, auth=auth, stream=False).text)
    follower_paginate_id = follower_user_ids['next_cursor']
    while follower_paginate_id != 0:
        get_follower_users = "https://api.twitter.com/1.1/followers/ids.json?screen_name=" + screen_name + "&count=5000&cursor=" + follower_paginate_id
        next_page_users = json.loads(requests.get(get_follower_users, auth=auth, stream=False).text)
        follower_user_ids['ids'].extend(next_page_users['ids'])
        follower_paginate_id = next_page_users['next_cursor']
    return follower_user_ids['ids']

# returns list of users following the 'screen_name' account
def get_following_users():
    following_user_ids = {}
    following_paginate_id = 0
    following_json_list_index = 0
    get_following_users = "https://api.twitter.com/1.1/friends/ids.json?cursor=-1&screen_name=" + screen_name + "&count=5000"
    following_user_ids = json.loads(requests.get(get_following_users, auth=auth, stream=False).text)
    following_paginate_id = following_user_ids['next_cursor']
    while following_paginate_id != 0:
        get_following_users = "https://api.twitter.com/1.1/friends/ids.json?screen_name=" + screen_name + "&count=5000&cursor=" + str(following_paginate_id)
        next_page_users = json.loads(requests.get(get_following_users, auth=auth, stream=False).text)
        following_user_ids['ids'].extend(next_page_users['ids'])
        following_paginate_id = next_page_users['next_cursor']
    return following_user_ids['ids']

def get_followers_without_followback():
    following = get_following_users()
    followers = get_follower_users()
    list_rejected_users = list(set(followers).difference(following))
    rejected_users_info = {}
    for i in range(0, len(list_rejected_users), 99):
        params = {'user_id': list_rejected_users[i:i+99]}
        url_get_user_objects = "https://api.twitter.com/1.1/users/lookup.json?"
        get_user_objects = json.loads(requests.get(url_get_user_objects, auth=auth, stream=False, params=params).text)
        for user in get_user_objects:
            rejected_users_info[user['id']] = '@' + user['screen_name']
    return rejected_users_info

if __name__ == "__main__":
    print(len(get_follower_users()))
    print(len(get_following_users()))
    print(len(get_followers_without_followback()))
    #except Exception as e:
        #print(e)

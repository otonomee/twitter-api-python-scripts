import json
import requests
from requests_oauthlib import OAuth1
import time
import random
import ApiKeys

access_token = ApiKeys.access_token
access_secret = ApiKeys.access_secret
consumer_key = ApiKeys.consumer_key
consumer_secret = ApiKeys.consumer_secret

# OAuth Authorization:
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
print(auth)

print("\n")
which_user = input("Follow Users of Screen Name: ")
#keyword = input("Keyword: ")
keywords = ['artist', 'musician', 'soundcloud', 'rapper', 'band', 'booking']
print("\n")


# Retrieves follower ID's, 15 requests every 15 minutes
ids = []
page_one = True
rate_exceeded = "{'errors': [{'message': 'Rate limit exceeded', 'code': 88}]}"
group_count = 0

# Adds user objects to each index Of 'ids' list
for i in range(15):
        if page_one ==  True:
                getfollowers = "https://api.twitter.com/1.1/followers/ids.json?cursor=-1&screen_name=" + str(which_user) + "&count=5000"
                ids.append(requests.get(getfollowers, auth=auth, stream=True).json())
                time.sleep(15)
                try:
                        if ids[i]['next_cursor'] == "":
                                break
                        else:
                                next_cursor = ids[i]['next_cursor']
                                page_one = False
                except KeyError:
                        print("Rate limit reached.")
                        print("\n")
                        raise SystemExit
        else:
                getfollowers = "https://api.twitter.com/1.1/followers/ids.json?&screen_name=" + str(which_user) + "&count=5000&cursor=" + str(next_cursor)
                ids.append(requests.get(getfollowers, auth=auth, stream=True).json())
                time.sleep(15)
                try:
                        next_cursor = ids[i]['next_cursor']
                except:
                        break


# Creates nested list of 100 users [[100 users], [100 users]...]
group_count = 0
ids_list = []
ids_full = []
mycounter = 0

for i in range(len(ids)):
        for my_id in ids[i]['ids']:
                if group_count <= 99:
                        group_count += 1
                        ids_list.append(my_id)
                else:
                        ids_full.append(ids_list)
                        ids_list = []
                        group_count = 0


for i in range(len(ids_full)):
        ids_full[i] = ",".join(str(x) for x in ids_full[i])

# Populates nested list of user objects
user_list = []
for i in range(len(ids_full)):
        getusers = "https://api.twitter.com/1.1/users/lookup.json?user_id=" + ids_full[i]
        users = requests.get(getusers, auth=auth, stream=True).json()
        time.sleep(15)
        user_list.append(users)


# [list index], [user index], [keyword]
# user_list[0][0]['description']

# Searches For Keyword In Each ID, Adds To New List
target_users = []
target_names = {}
for i in range(len(user_list)):
        for j in range((len(user_list[i]))):
                try:
                        if any(keyword in user_list[i][j]['description'] for keyword in keywords):
                                target_users.append(user_list[i][j]['id'])
                        elif any(keyword in user_list[i]['description'] for keyword in keywords):
                                target_users.append(user_list[i]['id'])
                except:
                        break

# Follows Users In 'target_users'

counter = 0
rate_limit = 0

for i in range(len(target_users)):
        rate_limit += 1
        if rate_limit > random.randint(49, 89):
                time.sleep(60)
                rate_limit = 0
        else:
                follow_users = "https://api.twitter.com/1.1/friendships/create.json?user_id=" + str(target_users[i]) + "&follow=true"
                follow_command = requests.post(follow_users, auth=auth, stream=True)
                rate_limit(60)
                print("Followed: " + str(target_users[i]))
                counter += 1
print("Followed " + str(counter) + " users.")

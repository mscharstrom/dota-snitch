#!/usr/bin/env python3

""" This app will be using the Steam API
to light a physical LED-Strip when X of Y
friends are in a specific game. """

import json
import requests
import setup


def get_friends():

    """ This will be the main function.
    From this data we will check how many
    friends that are in game and we'll
    decide if we should light the light """

    req = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={setup.STEAMAPI_KEY}&steamid={setup.MY_ID}&relationship=friend')
    friends_response = json.loads(req.content)

    # create  arrays for storing friends data
    friend_arr = set()
    dota_arr = set()
    online_arr = set()

    for friends in friends_response["friendslist"]["friends"]:
        friend_arr.add(friends["steamid"])

    # loop through friends and check their status, save to arrays.
    for friends in friend_arr:
        req_check = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={setup.STEAMAPI_KEY}&steamids={friends}')
        friends_check = json.loads(req_check.content)

        if "gameid" in friends_check["response"]["players"][0]:
            if friends_check["response"]["players"][0]["gameid"] == "570":
                dota_arr.add(friends_check["response"]["players"][0]["personaname"])
            elif friends_check["response"]["players"][0]["gameid"] != "570":
                online_arr.add(friends_check["response"]["players"][0]["personaname"])
        elif friends_check["response"]["players"][0]["personastate"] == 1:
            online_arr.add(friends_check["response"]["players"][0]["personaname"])

    print(("In Dota: ") + str(len(dota_arr)))
    print("Online: " + str(len(online_arr)))

    if (len(online_arr)) >= 2:
        get_light()
    elif (len(online_arr)) < 2:
        get_light_off()

def get_light():
    """This function lights the Hue
    up with PUT json request"""

    hue_url = 'http://{setup.HUE_IP}/api/{setup.HUE_ID}/lights/{setup.HUE_LIGHT}/state'

    data = {
            "on": "true",
            }
    headers = {"Content-Type": "application/json"}
    hue_response = requests.put(hue_url, data=json.dumps(data), headers=headers)

    print(hue_response.text)


def get_light_off():
    """This function lights the Hue
    up with PUT json request"""

    hue_url = 'http://{setup.HUE_IP}/api/{setup.HUE_ID}/lights/{setup.HUE_LIGHT}/state'

    data = {
            "on": "false",
            }
    headers = {"Content-Type": "application/json"}
    hue_response = requests.put(hue_url, data=json.dumps(data), headers=headers)

    print(hue_response.text)

if __name__ == '__main__':
    get_friends()

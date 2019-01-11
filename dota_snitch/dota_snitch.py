#!/usr/bin/env python3

""" This app will be using the Steam API
to light a physical LED-Strip when X of Y
friends are in a specific game. """

import json
import requests

STEAMAPI_KEY = ""  # Add your Steam API key
MY_ID = ""  # Add you Steam ID (in numbers).


def main():

    """ Test function to see my own status.
    This will be removed on first realease """

    req = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAMAPI_KEY}&steamids={MY_ID}')
    json_response = json.loads(req.content)

    personaname = json_response["response"]["players"][0]["personaname"]
    personastate = json_response["response"]["players"][0]["personastate"]

    print()
    print("name: " + personaname)
    print("state (online/offline etc): " + str(personastate))

    if "gameid" not in json_response["response"]["players"][0]:
        print("In game: None")
    else:
        persona_gameid = json_response["response"]["players"][0]["gameid"]
        print("In game: " + persona_gameid)


def get_friends():

    """ This will be the main function.
    From this data we will be starting
    the LED-Strip and make it light up """

    req = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={STEAMAPI_KEY}&steamid={MY_ID}&relationship=friend')
    friends_response = json.loads(req.content)

    print()
    print("Friends by SteamID:")

    # Save friends steam ID to an set array.
    friend_arr = set()
    for friends in friends_response["friendslist"]["friends"]:
        friend_arr.add(friends["steamid"])

    # Loop through friends and check their status
    for friends in friend_arr:
        req_check = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAMAPI_KEY}&steamids={friends}')
        friends_check = json.loads(req_check.content)

        if "gameid" in friends_check["response"]["players"][0]:
            if friends_check["response"]["players"][0]["gameid"] == "570":
                print(friends_check["response"]["players"][0]["personaname"] +
                      " - " + friends_check["response"]
                      ["players"][0]["gameid"])
            elif friends_check["response"]["players"][0]["gameid"] != "570":
                print(friends_check["response"]["players"][0]["personaname"] +
                      " - " + "Playing other game")
        elif friends_check["response"]["players"][0]["personastate"] == 1:
            print(friends_check["response"]["players"][0]["personaname"] +
                  " - Online")

if __name__ == '__main__':
    main()
    get_friends()

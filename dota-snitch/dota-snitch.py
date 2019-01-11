import json
import requests

steamapi_key = ""  # Add your Steam API key
my_id = ""  # Add you Steam ID (in numbers).

def main():
    req = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steamapi_key}&steamids={my_id}')
    json_response = json.loads(req.content)

    personaname_draft = json_response["response"]["players"][0]["personaname"]
    personastate_draft = json_response["response"]["players"][0]["personastate"]

    print()
    print("name: " + personaname_draft)
    print("state (online/offline etc): " + str(personastate_draft))


    if "gameid" not in json_response["response"]["players"][0]:
        print("In game: None")
    else:
        persona_game = json_response["response"]["players"][0]["gameid"]
        print("In game: " + persona_game)

    get_friends()

def get_friends():
    req = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?steamapi_key={steamapi_key}&steamid={my_id}&relationship=friend')
    friends_content = json.loads(req.content)

    print()
    print("Friends by SteamID:")

    # Save friends steam ID to an set array.
    friend_arr = set()
    for friends in friends_content["friendslist"]["friends"]:
        friend_arr.add(friends["steamid"])

    # Loop through friends and check their status
    for friends in friend_arr:
        req_check = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steamapi_key}&steamids={friends}')
        friends_check = json.loads(req_check.content)

        # Check if friend is online/in game 570 or online in game
        if "gameid" in friends_check["response"]["players"][0]:
           if friends_check["response"]["players"][0]["gameid"] == "570":
               print(friends_check["response"]["players"][0]["personaname"] + " - " + friends_check["response"]["players"][0]["gameid"])
           else:
               print(friends_check["response"]["players"][0]["personaname"] + " - " + "Playing other game")
        elif friends_check["response"]["players"][0]["personastate"] == 1:
            print(friends_check["response"]["players"][0]["personaname"] + " - Online")

if __name__ == '__main__':
    main()

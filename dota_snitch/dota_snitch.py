import json
import requests

STEAMAPI_KEY = "E175652E2DA8611CBCB169717B554130"  # Add your Steam API key
MY_ID = "76561198275301685"  # Add you Steam ID (in numbers).

def main():
    req = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAMAPI_KEY}&steamids={MY_ID}')
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
    req = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?steamapi_key={STEAMAPI_KEY}&steamid={MY_ID}&relationship=friend')
    friends_response = json.loads(req.content)

    print()
    print("Friends by SteamID:")

    # Save friends steam ID to an set array.
    friend_arr = set()
    for friends in friends_response["friendslist"]["friends"]:
        friend_arr.add(friends["steamid"])

    # Loop through friends and check their status
    for friend_id in friend_arr:
        req_check = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAMAPI_KEY}&steamids={friend_id}')
        friends_check = json.loads(req_check.content)

        if "gameid" in friends_check["response"]["players"][0]:
            if friends_check["response"]["players"][0]["gameid"] == "570":
                print(friends_check["response"]["players"][0]["personaname"] + " - " + friends_check["response"]["players"][0]["gameid"])
            elif friends_check["response"]["players"][0]["gameid"] != "570":
                print(friends_check["response"]["players"][0]["personaname"] + " - " + "Playing other game")
            elif friends_check["response"]["players"][0]["personastate"] == 1:
                print(friends_check["response"]["players"][0]["personaname"] + " - Online")
        else:
            print("No one Online")

if __name__ == '__main__':
    main()

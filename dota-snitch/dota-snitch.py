import json
import requests

key = "" # Add your Steam API key
myID = "" # Add you Steam ID (in numbers).

def main():
    req = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={myID}')
    jsonResponse = json.loads(req.content)

    personanameDraft = jsonResponse["response"]["players"][0]["personaname"]
    personastateDraft = jsonResponse["response"]["players"][0]["personastate"]

    print()
    print("name: " + personanameDraft)
    print("state (online/offline etc): " + str(personastateDraft))


    if "gameid" not in jsonResponse["response"]["players"][0]:
        print("In game: None")
    else:
        personaGame = jsonResponse["response"]["players"][0]["gameid"]
        print("In game: " + personaGame)

    get_friends()

def get_friends():
    req = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={key}&steamid={myID}&relationship=friend')
    friendsContent = json.loads(req.content)

    print()
    print("Friends by SteamID:")

    # Save friends steam ID to an set array.
    friendArr = set()
    for friends in friendsContent["friendslist"]["friends"]:
        friendArr.add(friends["steamid"])

    # Loop through friends and check their status
    for friends in friendArr:
        reqCheck = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={friends}')
        friendsCheck = json.loads(reqCheck.content)

        # Check if friend is online/in game 570 or online in game
        if "gameid" in friendsCheck["response"]["players"][0]:
           if friendsCheck["response"]["players"][0]["gameid"] == "570":
               print(friendsCheck["response"]["players"][0]["personaname"] + " - " + friendsCheck["response"]["players"][0]["gameid"])
           else:
               print(friendsCheck["response"]["players"][0]["personaname"] + " - " + "Playing other game")
        elif friendsCheck["response"]["players"][0]["personastate"] == 1:
            print(friendsCheck["response"]["players"][0]["personaname"] + " - Online")



if __name__ == '__main__':
    main()






from auth import client_id, client_secret, token, requests, json
from datetime import datetime, timedelta
# if __name__ == '__main__'

api_endpoint = "https://api.twitch.tv/helix/clips"
headers = {'Client-ID': client_id,
           "Authorization": "Bearer {}".format(token)}
first = 100
daysdiff = 2
d = datetime.utcnow() - timedelta(days=daysdiff)
started_at = d.isoformat("T") + "Z"

categories = {
    "League of Legends": "21779",
    "Just Chatting": "509658",
    "Fortnite": "33214",
    "COD MW": "512710",
    "Dota 2": "29595",
    "GTA V": "32982",
    "Minecraft": "27471",
    "CSGO": "32399",
    "Hyper Space": "518306",
    "Valorant": "516575",
    "WoW": "18122",
    "Tarkov": "491931",
    "Apex Legends": "511224",
    "Tarkov": "491931"
}

video_loc = "https://clips-media-assets2.twitch.tv/AT-cm%7C"


r = requests.get(api_endpoint + f'?game_id={categories["Fortnite"]}&first=100&started_at={started_at}',
                 headers=headers)
print(json.dumps(r.json()["data"], indent = 4))

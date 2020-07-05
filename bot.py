from auth import client_id, client_secret, token, requests, json
from datetime import datetime, timedelta
# if __name__ == '__main__'

def get_clips(daysdiff, game_name):
    d = datetime.utcnow() - timedelta(days=daysdiff)
    started_at = d.isoformat("T") + "Z"
    r = requests.get(api_endpoint + f'?game_id={categories[game_name]}&first=100&started_at={started_at}',
                     headers=headers)
    return r.json()["data"]

api_endpoint = "https://api.twitch.tv/helix/clips"
headers = {'Client-ID': client_id,
           "Authorization": "Bearer {}".format(token)}

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

unnecessary_stats = ["embed_url", "creator_id", "creator_name", "game_id",
                     "language", "view_count", "created_at", "thumbnail_url"]

clips = get_clips(2, "Fortnite")

for clip in clips:
    vid_id = clip["thumbnail_url"].split("-preview")[0] + ".mp4"
    clip["video_url"] = vid_id
    for stat in unnecessary_stats:
        del clip[stat]


print(json.dumps(clips, indent = 4))

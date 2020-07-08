from datetime import datetime, timedelta
from auth import *
from edit import video_length_seconds, get_total_length, change_fps, is_copyright, merge_videos
from upload_video import *
import os
# if __name__ == '__main__'

def get_clips_by_cat(daysdiff, category):
    d = datetime.utcnow() - timedelta(days=daysdiff)
    started_at = d.isoformat("T") + "Z"
    r = requests.get(api_endpoint + f'?game_id={categories[category]}&first=100&started_at={started_at}',
                     headers=headers)
    return r.json()["data"]

def get_clips_by_streamer(streamer, daysdiff):
    d = datetime.utcnow() - timedelta(days=daysdiff)
    started_at = d.isoformat("T") + "Z"
    d = datetime.utcnow()
    ended_at = d.isoformat("T") + "Z"

    r1 = requests.get("https://api.twitch.tv/helix/users?login={}".format(streamer), headers=headers)
    broadcaster_id = r1.json()["data"][0]["id"]

    r2 = requests.get(api_endpoint + f'?broadcaster_id={broadcaster_id}&first=100&started_at={started_at}&ended_at={ended_at}',
                     headers=headers)
    return r2.json()["data"]


def process_clips(clips, language):
    for clip in clips:
        vid_id = clip["thumbnail_url"].split("-preview")[0] + ".mp4"
        clip["video_url"] = vid_id
        for stat in unnecessary_stats:
            del clip[stat]

    processed_clips = [clip for clip in clips if language in clip["language"]]
    return processed_clips

def downloadfile(name, url, s, broadcaster_name, shoutouts):
    r=s.get(url)
    f=open(f'videos/{name}.mp4','wb');
    for chunk in r.iter_content(chunk_size=1024*1024):
        if chunk:
            f.write(chunk)
    f.close()
    if not is_copyright(name, re):
        shoutouts.add(broadcaster_name.lower())
        os.system(f'HandBrakeCLI -i /home/pelle/Bot/videos/{name}.mp4  Genius.flv -o /home/pelle/Bot/videos/out_{name}.mp4 --preset="Vimeo YouTube HQ 1080p60"')

    os.remove(f'videos/{name}.mp4')

def sort_clips_chronologically(arg):
    arg.sort(key=lambda k : k["created_at"])

def sort_clips_popularity(arg):
    arg.sort(key=lambda k : k["view_count"])

def make_video_by_cat(category, daysdiff = 1, sort_chron = False):
    clips = get_clips_by_cat(daysdiff, category)
    shoutouts = set()
    processed_clips = process_clips(clips, "en")
    title = processed_clips[0]["title"]

    if sort_chron:
        sort_clips_chronologically(processed_clips)

    print(json.dumps(processed_clips, indent = 4))

    with requests.Session() as s:
        for i, clip in enumerate(processed_clips):
            length = get_total_length()
            print(length)
            if length >= 601:
                break
            downloadfile(i, clip["video_url"], s, clip["broadcaster_name"], shoutouts)

    print(shoutouts)
    output_name = "video_output.mp4"
    merge_videos(output_name)
    upload_video(output_name, create_description(shoutouts), title, category)

def make_video_by_streamer(streamers, category = "", daysdiff = 1, sort_chron = True):
    clips = []
    for streamer in streamers:
        clips += get_clips_by_streamer(streamer, daysdiff)
    if sort_chron:
        clips = clips[:120]
        sort_clips_chronologically(clips)

    if category:
        pass
    else:
        processed_clips = clips

    print(json.dumps(processed_clips, indent = 4))

    with requests.Session() as s:
        for i, clip in enumerate(processed_clips):
            length = get_total_length()
            print(length)
            if length >= 601:
                break
            downloadfile(i, clip["video_url"], s, clip["broadcaster_name"], shoutouts)

    print(shoutouts)
    output_name = "video_output.mp4"
    merge_videos(output_name)
    upload_video(output_name, create_description(shoutouts), title, category)

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


unnecessary_stats = ["embed_url", "creator_id", "creator_name", "game_id", "thumbnail_url"]

#make_video_by_cat("Fortnite")
print(json.dumps(get_clips_by_streamer("tfue", 1000), indent = 4))

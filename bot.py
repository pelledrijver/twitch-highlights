from datetime import datetime, timedelta
from auth import *
from edit import video_length_seconds, get_total_length, change_fps, is_copyright, merge_videos
from upload_video import *
from random import randrange
import os
# if __name__ == '__main__'


auth = createAuthObject()


def get_clips_by_cat(daysdiff, category):
    d = datetime.utcnow() - timedelta(days=daysdiff)
    started_at = d.isoformat("T") + "Z"
    r = requests.get(auth.twitch_api_endpoint + f'?game_id={categories[category]}&first=100&started_at={started_at}',
                     headers=auth.twitchHeader)
    return r.json()["data"]

def get_clips_by_streamer(streamer, daysdiff):
    d = datetime.utcnow() - timedelta(days=daysdiff)
    started_at = d.isoformat("T") + "Z"
    d = datetime.utcnow()
    ended_at = d.isoformat("T") + "Z"

    r1 = requests.get("https://api.twitch.tv/helix/users?login={}".format(streamer), headers=auth.twitchHeader)
    broadcaster_id = r1.json()["data"][0]["id"]

    r2 = requests.get(auth.twitch_api_endpoint + f'?broadcaster_id={broadcaster_id}&first=100&started_at={started_at}&ended_at={ended_at}',
                     headers=auth.twitchHeader)
    return r2.json()["data"]


def filter_clips(clips, language):
    for clip in clips:
        vid_id = clip["thumbnail_url"].split("-preview")[0] + ".mp4"
        clip["video_url"] = vid_id
        for stat in unnecessary_stats:
            del clip[stat]

    filtered_clips = [clip for clip in clips if language in clip["language"]]
    return filtered_clips

def downloadfile(name, url, s, broadcaster_name, shoutouts):
    r=s.get(url)
    f=open(f'videos/{name}.mp4','wb');
    for chunk in r.iter_content(chunk_size=1024*1024):
        if chunk:
            f.write(chunk)
    f.close()
    if not is_copyright(name, auth.copyright_recognizer):
        shoutouts.add(broadcaster_name.lower())
        os.system(f'HandBrakeCLI -i videos/{name}.mp4  -o videos/out_{name}.mp4 --preset="Vimeo YouTube HQ 1080p60" --width 1920 --height 1080')

    os.remove(f'videos/{name}.mp4')

def sort_clips_chronologically(arg):
    arg.sort(key=lambda k : k["created_at"])

def sort_clips_popularity(arg):
    arg.sort(key=lambda k : k["view_count"])

def make_video_by_cat(category, daysdiff = 1, sort_chron = False, uploadtime_diff = 1, custom_title=""):
    clips = get_clips_by_cat(daysdiff, category)
    shoutouts = set()
    filtered_clips = filter_clips(clips, "en")

    if custom_title:
        title = custom_title
    else:
        title = filtered_clips[0]["title"].title() + " - {} Highlights".format(category)

    if sort_chron:
        sort_clips_chronologically(filtered_clips)

    print(json.dumps(filtered_clips, indent = 4))

    with requests.Session() as s:
        maxLength = 270 + randrange(50)
        for i, clip in enumerate(filtered_clips, 10):
            length = get_total_length()
            print(length)
            if length >= maxLength:
                break
            downloadfile(i, clip["video_url"], s, clip["broadcaster_name"], shoutouts)

    print(shoutouts)
    output_name = "video_output.mp4"
    merge_videos(output_name)
    upload_video(output_name, create_description(shoutouts), title, category, timedelta(hours=uploadtime_diff))

def make_video_by_streamer(streamers, category = "", daysdiff = 1, sort_chron = True, uploadtime_diff = timedelta(hours=1), custom_title = ""):
    clips = []
    shoutouts = set()

    for streamer in streamers:
        clips += get_clips_by_streamer(streamer, daysdiff)

    if category:
        clips = [clip for clip in clips if categories[category] == clip["game_id"]]

    if sort_chron:
        clips = clips[:120]
        sort_clips_chronologically(clips)

    filtered_clips = filter_clips(clips, "en")
    print(json.dumps(filtered_clips, indent = 4))

    if custom_title:
        title = custom_title
    else:
        title = filtered_clips[0]["title"].title() + " - {} Highlights".format(category)

    maxLength = 270 + randrange(50)
    with requests.Session() as s:
        for i, clip in enumerate(filtered_clips, 10):
            length = get_total_length()
            print(length)
            if length >= maxLength:
                break
            downloadfile(i, clip["video_url"], s, clip["broadcaster_name"], shoutouts)

    print(shoutouts)
    output_name = "video_output.mp4"
    merge_videos(output_name)
    upload_video(output_name, create_description(shoutouts), title, category, timedelta(hours=uploadtime_diff))


categories = {
    "League of Legends": "21779",
    "Just Chatting": "509658",
    "Fortnite": "33214",
    "Call of Duty Modern Warfare": "512710",
    "Dota 2": "29595",
    "GTA V": "32982",
    "Minecraft": "27471",
    "CSGO": "32399",
    "Hyperscape": "518306",
    "Valorant": "516575",
    "WoW": "18122",
    "Tarkov": "491931",
    "Apex Legends": "511224",
    "Tarkov": "491931",
    "Fall Guys": "512980",
    "Among Us": "510218"
}


unnecessary_stats = ["embed_url", "creator_id", "creator_name", "thumbnail_url"]



make_video_by_cat("Among Us", uploadtime_diff=2.5)
make_video_by_cat("Just Chatting", uploadtime_diff=5)
make_video_by_cat("Valorant", uploadtime_diff=7.5);

#make_video_by_cat("Among Us", uploadtime_diff=11, daysdiff=30, custom_title = "Most-watched Among Us clips of the month")

os.system("shutdown now")

#make_video_by_cat("Minecraft", uploadtime_diff=16)


#make_video_by_streamer(["greekgodx"], daysdiff = 30, sort_chron = False, custom_title = "greekgodx shows his thick legs", uploadtime_diff=10)
#make_video_by_streamer(["tfue"], daysdiff = 2, sort_chron = False, custom_title="tfue and cloak DOMINATE Warzone tournament", uploadtime_diff = 13, category = "Call of Duty Modern Warfare")


#make_video_by_streamer(["thor"], daysdiff = 30, sort_chron = False, custom_title = "HYPERSCAPE CLIPS THAT MADE THOR FAMOUS", uploadtime_diff=6)

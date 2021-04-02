from datetime import datetime, timedelta
from auth import *
from edit import *
from random import randrange
import tempfile
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

# if __name__ == '__main__'


auth = createAuthObject()
tmpdir = tempfile.mkdtemp()

def get_top_categories():
    response = requests.get("https://api.twitch.tv/helix/games/top", headers=auth.twitchHeader).json()['data']
    category_dict = dict()
    for category in response:
        category_dict[category['name']] = category['id']

    return category_dict


def get_clips_by_cat(daysdiff, category):
    time_interval_start = datetime.utcnow() - timedelta(days=daysdiff)
    started_at = time_interval_start.isoformat("T") + "Z"
    response = requests.get(auth.twitch_api_endpoint + f'?game_id={categories[category]}&first=100&started_at={started_at}',
                     headers=auth.twitchHeader)
    return response.json()["data"]

def get_clips_by_streamer(streamer, daysdiff):
    time_interval_start = datetime.utcnow() - timedelta(days=daysdiff)
    started_at = time_interval_start.isoformat("T") + "Z"
    time_interval_end = datetime.utcnow()
    ended_at = time_interval_end.isoformat("T") + "Z"

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

def downloadfile(name, url, s, broadcaster_name):
    file_path = f'{tmpdir}/{name}.mp4'


    r=s.get(url)
    f=open(file_path,'wb');
    for chunk in r.iter_content(chunk_size=1024*1024):
        if chunk:
            f.write(chunk)
    f.close()

    return file_path


def sort_clips_chronologically(arg):
    arg.sort(key=lambda k : k["created_at"])

def sort_clips_popularity(arg):
    arg.sort(key=lambda k : k["view_count"])


def make_video_from_json(output_name, clips_json):
    print("Succesfully fetched clip data")

    clip_list = []

    maxLength = 270 + randrange(50)
    with requests.Session() as s:
        for i, clip in enumerate(clips_json, 10):
            if get_merged_length(clip_list) >= maxLength:
                break
            
            print(f'Downloading clip: {clip["broadcaster_name"]} - {clip["title"]}')
            file_name = downloadfile(i, clip["video_url"], s, clip["broadcaster_name"])
            add_clip(clip_list, file_name)

    output_name = "video_output"
    merge_videos(clip_list, output_name, tmpdir)


def make_video_by_cat(category, daysdiff = 1, sort_chron = False, uploadtime_diff = 1, custom_title="", output_name="video_output"):
    clips = get_clips_by_cat(daysdiff, category)
    shoutouts = set()
    filtered_clips = filter_clips(clips, "en")

    if custom_title:
        title = custom_title
    else:
        title = filtered_clips[0]["title"].title() + " - {} Highlights".format(category)

    if sort_chron:
        sort_clips_chronologically(filtered_clips)

    make_video_from_json(output_name, filtered_clips)


def make_video_by_streamer(streamers, category = "", daysdiff = 1, sort_chron = True, uploadtime_diff = timedelta(hours=1), custom_title = "", output_name="video_output"):
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

    make_video_from_json(output_name, filtered_clips)
    


categories = get_top_categories()



make_video_by_cat("Among Us", uploadtime_diff=2.5)
make_video_by_cat("Just Chatting", uploadtime_diff=5)
make_video_by_cat("Valorant", uploadtime_diff=7.5);

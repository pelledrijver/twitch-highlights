from moviepy.editor import VideoFileClip, concatenate_videoclips
from slugify import slugify
from tqdm import tqdm
import tempfile
import random
import proglog
import requests
import os
import shutil
from . import acr_cloud


def sort_clips_chronologically(clips):
    clips.sort(key=lambda k: k["created_at"])


def sort_clips_popularity(clips):
    clips.sort(key=lambda k: k["view_count"], reverse=True)


def sort_clips_randomly(clips):
    clips.sort(random.shuffle(clips))


def add_clip(clip_list, file_path, render_settings):
    if len(clip_list) == 0 and 'intro_path' in render_settings:
        clip_list.append(
            VideoFileClip(render_settings['intro_path'], target_resolution=render_settings["target_resolution"]))

    if 'transition_path' in render_settings and len(clip_list) != 0:
        clip_list.append(
            VideoFileClip(render_settings['transition_path'], target_resolution=render_settings["target_resolution"]))

    clip_list.append(VideoFileClip(file_path, target_resolution=render_settings["target_resolution"]))


def download_clip(session, clip, file_path):
    video_url = clip["video_url"]

    response = session.get(video_url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

    f = open(file_path, 'wb')
    for chunk in response.iter_content(chunk_size=1024 * 1024):
        if chunk:
            progress_bar.update(len(chunk))
            f.write(chunk)
    f.close()
    progress_bar.close()


def get_combined_video_length(clip_list):
    sum = 0
    for clip in clip_list:
        sum += clip.duration
    return sum


def check_render_settings(render_settings):
    if render_settings is None:
        render_settings = dict()
        render_settings["fps"] = 60
        render_settings["target_resolution"] = (1080, 1920)
        return render_settings

    if 'fps' not in render_settings:
        render_settings['fps'] = 60

    if 'target_resolution' not in render_settings:
        render_settings['target_resolution'] = (1080, 1920)

    if 'intro_path' in render_settings:
        temp = VideoFileClip(render_settings['intro_path'], target_resolution=render_settings["target_resolution"])
        temp.close()

    if 'outro_path' in render_settings:
        temp = VideoFileClip(render_settings['outro_path'], target_resolution=render_settings["target_resolution"])
        temp.close()

    if 'transition_path' in render_settings:
        temp = VideoFileClip(render_settings['transition_path'], target_resolution=render_settings["target_resolution"])
        temp.close()

    return render_settings


def merge_videos(clip_list, output_name, render_settings):
    if len(clip_list) == 0:
        raise Exception("No clips have been found with the specified preferences. "
                        "Try different preferences instead.")

    if 'outro_path' in render_settings:
        clip_list.append(
            VideoFileClip(render_settings['outro_path'], target_resolution=render_settings["target_resolution"]))

    merged_video = concatenate_videoclips(clip_list, method="compose")
    temp_dir_path = get_temp_dir()
    print(f"Writing video file to {output_name}.mp4")

    merged_video.write_videofile(
        f"{output_name}.mp4",
        codec="libx264",
        fps=render_settings['fps'],
        temp_audiofile=os.path.join(temp_dir_path, "temp-audio.m4a"),
        remove_temp=True,
        audio_codec="aac",
        logger=proglog.TqdmProgressBarLogger(print_messages=False))

    merged_video.close()
    for clip in clip_list:
        clip.close()

    print(f'Successfully generated highlight video "{output_name}"!')


def preprocess_clips(clips, language):
    for clip in clips:
        video_url = clip["thumbnail_url"].split("-preview")[0] + ".mp4"
        clip["video_url"] = video_url

    if language is not None:
        return [clip for clip in clips if language in clip["language"]]

    return clips


def create_video_from_json(clips, output_name, language, video_length, render_settings, sort_by, filter_copyright,
                           acr_credentials=None):
    print("Successfully fetched clip data")

    remove_tmp_content()
    temp_dir_path = get_temp_dir()
    clips = preprocess_clips(clips, language)
    render_settings = check_render_settings(render_settings)

    if sort_by == "random":
        sort_clips_randomly(clips)
    elif sort_by == "popularity":
        sort_clips_popularity(clips)
    elif sort_by == "chronologically":
        sort_clips_chronologically(clips)
    else:
        Exception(f'Sorting method {sort_by} not recognized.')

    clip_list = []

    with requests.Session() as s:
        for clip in clips:
            if get_combined_video_length(clip_list) >= video_length:
                break

            print(f'Downloading clip: {clip["broadcaster_name"]} - {clip["title"]}')
            file_name = slugify(f'{clip["title"]} - {clip["video_id"]}')
            file_path = os.path.join(temp_dir_path, f'{file_name}.mp4')
            download_clip(s, clip, file_path)

            if filter_copyright:
                print("Checking for copyrighted music...")

                if acr_cloud.is_copyright(file_path, acr_credentials):
                    print("Copyrighted music has been detected in clip. Clip removed!")
                    os.remove(file_path)
                    continue
                else:
                    print("No copyrighted music has been found!")

            add_clip(clip_list, file_path, render_settings)

    merge_videos(clip_list, output_name, render_settings)

    shutil.rmtree(temp_dir_path)


def remove_tmp_content():
    temp_dir_path = get_temp_dir()

    if os.path.isdir(temp_dir_path):
        shutil.rmtree(temp_dir_path)
    os.mkdir(temp_dir_path)


def get_temp_dir():
    temp_dir_path = os.path.join(tempfile.gettempdir(), "twitch_highlights")
    return temp_dir_path

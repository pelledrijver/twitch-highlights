import os
from pathlib import Path
import subprocess
import os, sys
import json
from moviepy.editor import VideoFileClip, concatenate_videoclips


def get_merged_length(clip_list):
    return sum(clip.duration for clip in clip_list)



def add_clip(clip_list, path, target_resolution = (1080, 1920)):
    clip_list = clip_list.append(VideoFileClip(path, target_resolution=target_resolution))


def merge_videos(clip_list, output_name, video_path):
    merged_video = concatenate_videoclips(clip_list, method="compose")

    merged_video.write_videofile(
            f"{output_name}.mp4",
            codec="libx264",
            fps=60,
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            audio_codec="aac")

    for clip in clip_list:
        clip.close()
    merged_video.close()


    for file in os.listdir(video_path):
        if file.endswith(".mp4"):
            os.remove(os.path.join(video_path, file))

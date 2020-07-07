import os
from pathlib import Path
import subprocess

import os, sys
from acrcloud.recognizer import ACRCloudRecognizer
from acrcloud.recognizer import ACRCloudRecognizeType
import json


def video_length_seconds(filename):
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            filename,
        ],
        capture_output=True,
        text=True,
    )
    try:
        return float(result.stdout)
    except ValueError:
        raise ValueError(result.stderr.rstrip("\n"))

length = 0

def get_total_length():
    return sum(video_length_seconds(f) for f in Path("./videos").iterdir() if f.is_file())

def change_fps():
    pass

def is_copyright(name, re):
    path = f'videos/{name}.mp4'
    result = json.loads(re.recognize_by_file(path, 0, 10))
    return result["status"]["msg"] != "No result"


def merge_videos():
    os.system("find videos/*.mp4 | sed 's:\ :\\\ :g'| sed 's/^/file /' > fl.txt; ffmpeg -f concat -i fl.txt -c copy apex_output.mp4; rm fl.txt")
    filelist = [ f for f in os.listdir("./videos") if f.endswith(".mp4") ]
    for f in filelist:
        os.remove(os.path.join("./videos", f))


#videos = [f for f in os.listdir("./videos") if os.path.isfile(os.path.join("./videos", f))]
#videos.sort()
#for video in videos:
#    os.system(f'ffmpeg -i ./videos/{video} -r 60 ./videos/new_{video}')

#find videos/*.mp4 | sed 's:\ :\\\ :g'| sed 's/^/file /' > fl.txt; ffmpeg -f concat -i fl.txt -c copy output.mp4; rm fl.txt

#video to audio:
#ffmpeg -y -i [input] -ac 1 -ar 8000 -ss [offset] -t [duration] out.wav
#HandBrakeCLI -i /home/pelle/Bot/videos/3.mp4  Genius.flv -o /home/pelle/Bot/videos/new_3.mp4 --preset="Vimeo YouTube HQ 1080p60"

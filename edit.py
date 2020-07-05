import os
from pathlib import Path
import subprocess



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

#videos = [f for f in os.listdir("./videos") if os.path.isfile(os.path.join("./videos", f))]
#videos.sort()
#for video in videos:
#    os.system(f'ffmpeg -i ./videos/{video} -r 60 ./videos/new_{video}')

#find videos/*.mp4 | sed 's:\ :\\\ :g'| sed 's/^/file /' > fl.txt; ffmpeg -f concat -i fl.txt -c copy output.mp4; rm fl.txt

import os

def upload_video(filename):
    os.system('./youtubeuploader -filename {}'.format(filename))
    os.remove(filename)

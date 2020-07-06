from apiclient.discovery import build


def create_yt_obj(yt_key):
    youtube = build('youtube', 'v3', developerKey = yt_key)
    return youtube

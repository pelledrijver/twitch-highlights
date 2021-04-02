import requests, json


class Auth:
    twitch_api_endpoint = "https://api.twitch.tv/helix/clips"

    def __init__(self, twitch_token, twitch_client_id, copyright_recognizer, yt_key):
        self.twitch_token = twitch_token
        self.copyright_recognizer = copyright_recognizer
        self.yt_key = yt_key
        self.twitchHeader = {'Client-ID': twitch_client_id,
                        "Authorization": "Bearer {}".format(twitch_token)}

def createAuthObject():
    f_secrets = open('secrets.txt', 'r')

    twitch_client_id = f_secrets.readline().strip()
    twitch_client_secret = f_secrets.readline().strip()
    acr_host = f_secrets.readline().strip()
    acr_key = f_secrets.readline().strip()
    acr_secret = f_secrets.readline().strip()
    yt_key = f_secrets.readline().strip()
    f_secrets.close()

    twitch_oauth_endpoint = "https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type={}".format(
                      twitch_client_id, twitch_client_secret, "client_credentials")

    twitch_oauth_reply  = requests.post(twitch_oauth_endpoint).json()
    twitch_token = twitch_oauth_reply['access_token']

    copyright_recognizer = None

    return Auth(twitch_token, twitch_client_id, copyright_recognizer, yt_key)

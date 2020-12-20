import requests, json
from acrcloud.recognizer import ACRCloudRecognizer
from acrcloud.recognizer import ACRCloudRecognizeType


class Auth:
    twitch_api_endpoint = "https://api.twitch.tv/helix/clips"

    def __init__(self, twitch_token, twitch_client_id, copyright_recognizer, yt_key):
        # self.twitch_token = twitch_token
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

    oauth_endpoint = "https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type={}".format(
                      twitch_client_id, twitch_client_secret, "client_credentials")

    oauth_reply  = requests.post(oauth_endpoint).json()
    twitch_token = oauth_reply['access_token']

    ACR_config = {
        'host':acr_host,
        'access_key':acr_key,
        'access_secret':acr_secret,
        'recognize_type': ACRCloudRecognizeType.ACR_OPT_REC_AUDIO,
        'debug':False,
        'timeout':10 # seconds
    }

    copyright_recognizer = ACRCloudRecognizer(ACR_config)

    return Auth(twitch_token, twitch_client_id, copyright_recognizer, yt_key)

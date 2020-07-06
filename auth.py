import requests
import json

import os, sys
from acrcloud.recognizer import ACRCloudRecognizer
from acrcloud.recognizer import ACRCloudRecognizeType


f_secrets = open('secrets.txt', 'r')

client_id = f_secrets.readline().strip()
client_secret = f_secrets.readline().strip()
acr_host = f_secrets.readline().strip()
acr_key = f_secrets.readline().strip()
acr_secret = f_secrets.readline().strip()
yt_key = f_secrets.readline().strip()
f_secrets.close()

postlink = "https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type={}".format(
            client_id, client_secret, "client_credentials")

r  = requests.post(postlink)
data = r.json()
token = data['access_token']


config = {
    'host':acr_host,
    'access_key':acr_key,
    'access_secret':acr_secret,
    'recognize_type': ACRCloudRecognizeType.ACR_OPT_REC_AUDIO, # you can replace it with [ACR_OPT_REC_AUDIO,ACR_OPT_REC_HUMMING,ACR_OPT_REC_BOTH], The     SDK decide which type fingerprint to create accordings to "recognize_type".
    'debug':False,
    'timeout':10 # seconds
}

re = ACRCloudRecognizer(config)

#print("Auth succesful")

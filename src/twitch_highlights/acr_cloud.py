from moviepy.editor import VideoFileClip
import os
import base64
import hmac
import hashlib
import time
import requests


# https://docs.acrcloud.com/reference/identification-api

def login(acr_credentials):
    access_key = acr_credentials["access_key"]
    access_secret = acr_credentials["secret_key"]

    requrl = f'https://{acr_credentials["host"]}/v1/identify'
    timestamp = time.time()

    string_to_sign = f'POST\n/v1/identify\n{access_key}\naudio\n1\n{str(timestamp)}'
    sign = base64.b64encode(hmac.new(bytes(access_secret, encoding="utf8"), bytes(string_to_sign, encoding="utf8"),
                                     digestmod=hashlib.sha1).digest())

    data = {'access_key': access_key,
            'sample_bytes': 0,
            'timestamp': str(timestamp),
            'signature': sign,
            'data_type': "audio",
            "signature_version": "1"}

    response = requests.post(requrl, files=None, data=data)

    if response.status_code != 200:
        raise Exception(f'An error occured while authenticating ACRCloud: {response.json()}')

    if response.json()["status"]["code"] != 3006:
        raise Exception("An error occured while authenticating ACRCloud: invalid credentials",
                        response.json()["status"]["msg"])

    return acr_credentials


def is_copyright(file_path, acr_credentials):
    access_key = acr_credentials["access_key"]
    access_secret = acr_credentials["secret_key"]
    requrl = f'https://{acr_credentials["host"]}/v1/identify'

    temp_dir = os.path.dirname(os.path.realpath(file_path))
    audio_file_path = os.path.join(temp_dir, 'temp.mp3')

    video = VideoFileClip(file_path)
    audio = video.audio
    audio.write_audiofile(audio_file_path, logger=None)
    audio.close()
    video.close()

    timestamp = time.time()

    string_to_sign = f'POST\n/v1/identify\n{access_key}\naudio\n1\n{str(timestamp)}'
    sign = base64.b64encode(hmac.new(bytes(access_secret, encoding="utf8"), bytes(string_to_sign, encoding="utf8"),
                                     digestmod=hashlib.sha1).digest())

    f = open(audio_file_path, "rb")
    sample_bytes = os.path.getsize(audio_file_path)

    files = [
        ('sample', ('temp.mp3', f, 'audio/mpeg'))
    ]
    data = {'access_key': access_key,
            'sample_bytes': sample_bytes,
            'timestamp': str(timestamp),
            'signature': sign,
            'data_type': "audio",
            "signature_version": "1"}

    response = requests.post(requrl, files=files, data=data)
    response.encoding = "utf-8"

    f.close()
    os.remove(audio_file_path)

    if response.status_code != 200:
        raise Exception(response.json())

    error_code = response.json()["status"]["code"]

    if error_code != 0 and error_code != 1001:
        raise Exception(response.json()["status"]["msg"])

    return error_code == 0

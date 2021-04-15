from moviepy.editor import VideoFileClip
import os
import base64
import hmac
import hashlib
import time
import requests 


def check_acr_credentials(acr_credentials):
    pass


def isCopyright(file_path, acr_credentials):
    access_key = acr_credentials["access_key"]
    access_secret = acr_credentials["secret_key"]
    requrl = f'https://{acr_credentials["host"]}/v1/identify'
    
    temp_dir = os.path.dirname(os.path.realpath(file_path))
    audio_file_path = os.path.join(temp_dir, 'temp.mp3')
    
    video = VideoFileClip(file_path)
    audio = video.audio
    audio.write_audiofile(audio_file_path)
    audio.close()
    video.close()

    http_method = "POST"
    http_uri = "/v1/identify"

    data_type = "audio"
    signature_version = "1"
    timestamp = time.time()

    string_to_sign = http_method+"\n"+http_uri+"\n"+access_key+"\n"+data_type+"\n"+signature_version+"\n"+str(timestamp)
    sign = base64.b64encode(hmac.new(bytes(access_secret, encoding="utf8"),bytes(string_to_sign, encoding="utf8"), digestmod=hashlib.sha1).digest())

    f = open(audio_file_path, "rb")
    sample_bytes = os.path.getsize(audio_file_path)

    files=[
    ('sample',('temp.mp3',f,'audio/mpeg'))
    ]
    data = {'access_key':access_key,
            'sample_bytes':sample_bytes,
            'timestamp':str(timestamp),
            'signature':sign,
            'data_type':data_type,
            "signature_version":signature_version}

    r = requests.post(requrl, files=files, data=data)
    r.encoding = "utf-8"
    
    f.close()
    os.remove(audio_file_path)
    print (r.text)
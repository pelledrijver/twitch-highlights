import requests
import json

f_secrets = open('secrets.txt', 'r')

client_id = f_secrets.readline().strip()
client_secret = f_secrets.readline().strip()
f_secrets.close()

postlink = "https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type={}".format(
            client_id, client_secret, "client_credentials")


r  = requests.post(postlink)
data = r.json()
token = data['access_token']

#print("Auth succesful")
#https://id.twitch.tv/oauth2/token?client_id=bmbdun9wx214a6x51gxgquqve5jpkm&client_secret=ekv0vasa0v2js2uh84pxnl0v5wxpd5&grant_type=client_credentials
#r = requests.get("https://api.twitch.tv/helix/games/top", headers = headers)
#print(json.dumps(r.json(), indent = 4))

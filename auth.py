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

from twitch_highlights import TwitchHighlights

twitch_credentials = {
    "client_id": "##############################",             # Your client id here
    "client_secret": "##############################"          # Your client secret here
}

acr_credentials = {
    "access_key": "################################",          # Your access key here
    "secret_key": "########################################",  # Your secret key here   
    "host": "###############################"                  # Your host here
}

highlight_generator = TwitchHighlights(twitch_credentials=twitch_credentials, acr_credentials=acr_credentials)

highlight_generator.make_video_by_category(category="Music", filter_copyright=True)

from twitch_highlights import TwitchHighlights

twitch_credentials = {
    "client_id": "##############################",       # Your client id here
    "client_secret": "##############################"    # Your client secret here
}

highlight_generator = TwitchHighlights(twitch_credentials=twitch_credentials)

highlight_generator.make_video_by_category(category="Fortnite")

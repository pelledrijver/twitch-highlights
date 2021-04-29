from twitch_highlights import TwitchHighlights

highlight_generator = TwitchHighlights({
    "client_id": "##############################",       # Your client id here   
    "client_secret": "##############################"    # Your client secret here   
})

highlight_generator.make_video_by_category(category = "Fortnite")
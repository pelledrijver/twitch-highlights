from twitch_highlights import TwitchHighlights
from datetime import datetime, timedelta

twitch_credentials = {
    "client_id": "##############################",      # Your client id here
    "client_secret": "##############################"   # Your client secret here
}

render_settings = {
    'intro_path': "##############################",     # Path to intro video file
    'outro_path': "##############################",     # Path to outro video file
    'transition_path': "##############################" # Path to transition video file
}

started_at = datetime.utcnow() - timedelta(days=7)      # Starting date/time for included clips. Currently set to one week ago.
ended_at = datetime.utcnow() - timedelta(days=1)        # Ending date/time for included clips. Currently set to one week ago.

highlight_generator = TwitchHighlights(twitch_credentials=twitch_credentials)

highlight_generator.make_video_by_category(category="Fortnite", output_name="epic_highlight_video",
                                           language="fr", video_length=100, started_at=started_at,
                                           ended_at=ended_at, render_settings=render_settings,
                                           sort_by="chronologically")

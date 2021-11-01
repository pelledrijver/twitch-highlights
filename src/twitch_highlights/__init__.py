from datetime import datetime, timedelta
from . import twitch_api
from . import clip_edit
from . import acr_cloud


class TwitchHighlights:
    def __init__(self, twitch_credentials, acr_credentials=None):
        self.twitch_oauth_header = twitch_api.login(twitch_credentials)

        if acr_credentials:
            self.acr_credentials = acr_cloud.login(acr_credentials)

    def get_top_categories(self, amount=20):
        return twitch_api.get_top_categories(self.twitch_oauth_header, amount)

    def make_video_by_category(self, category, output_name="output_video", language=None, video_length=300,
                               started_at=datetime.utcnow() - timedelta(days=1), ended_at=datetime.utcnow(),
                               render_settings=None, sort_by="popularity", filter_copyright=False):
        acr_credentials = None
        if filter_copyright:
            self.check_acr_cloud_credentials()
            acr_credentials = self.acr_credentials

        clips = twitch_api.get_clips_by_category(self.twitch_oauth_header, category, started_at, ended_at)
        clip_edit.create_video_from_json(clips, output_name, language, video_length, render_settings, sort_by,
                                         filter_copyright, acr_credentials)

    def make_video_by_streamer(self, streamers, output_name="output_video", language=None, video_length=300,
                               started_at=datetime.utcnow() - timedelta(days=1), ended_at=datetime.utcnow(),
                               render_settings=None, sort_by="popularity", filter_copyright=False):
        acr_credentials = None
        if filter_copyright:
            self.check_acr_cloud_credentials()
            acr_credentials = self.acr_credentials

        clips = []
        for streamer in streamers:
            clips.extend(twitch_api.get_clips_by_streamer(self.twitch_oauth_header, streamer, started_at, ended_at))

        clip_edit.create_video_from_json(clips, output_name, language, video_length, render_settings, sort_by,
                                         filter_copyright, acr_credentials)

    def check_acr_cloud_credentials(self):
        if not hasattr(self, "acr_credentials"):
            raise Exception("No ACRCloud credentials have been found. Please make sure to pass the ACR credentials "
                            "to the TwitchHighlights constructor.")

from moviepy.editor import VideoFileClip
from datetime import datetime, timedelta
import requests
import shutil
import os
import time
import twitch_api
import clip_edit

#maybe do all checks in here (including render settings)


class TwitchHighlights:
    def __init__(self, twitch_credentials = None):
        if(twitch_credentials):
            self.login_twitch(twitch_credentials)   


    def login_twitch(self, twitch_credentials):
        self.twitch_oauth_header = twitch_api.login(twitch_credentials)


    def get_top_categories(self, amount = 20):
        self.check_twitch_authentication()
        return twitch_api.get_top_categories(self.twitch_oauth_header, amount)


    def make_video_by_category(self, category, output_name = "output_video", language = None, video_length = 300, started_at = datetime.utcnow() - timedelta(days=1), ended_at = datetime.utcnow(), render_settings = None, sort_by = "popularity"):
        self.check_twitch_authentication()
        
        clips = twitch_api.get_clips_by_category(self.twitch_oauth_header, category, started_at, ended_at)
        clip_edit.create_video_from_json(clips, output_name, language, video_length, render_settings, sort_by)


    def make_video_by_streamer(self, streamers, output_name = "output_video", language = None, video_length = 300, started_at = datetime.utcnow() - timedelta(days=1), ended_at = datetime.utcnow(), render_settings = None, sort_by = "popularity"):
        self.check_twitch_authentication()

        clips = [twitch_api.get_clips_by_streamer(self.twitch_oauth_header, streamer, started_at, ended_at) for streamer in streamers]
        clip_edit.create_video_from_json(clips, output_name, language, video_length, render_settings, sort_by)


    # def _create_video_from_json(self, clips, output_name, language, video_length, render_settings, sort_by):
    #     clip_edit.create_video_from_json(clips, output_name, language, video_length, render_settings, sort_by)

    def check_twitch_authentication(self):
        if not hasattr(self, "twitch_oauth_header"):
            raise Exception("Twitch authentication incomplete. Please authenticate using the login_twitch() method.")

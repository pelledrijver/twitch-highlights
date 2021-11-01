# twitch-highlights
[![GitHub](https://img.shields.io/github/license/pelledrijver/twitch-highlights)](https://github.com/pelledrijver/twitch-highlights/blob/master/LICENSE)
[![PyPI Project](https://img.shields.io/pypi/v/twitch-highlights)](https://pypi.org/project/twitch-highlights/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/twitch-highlights)](https://pypi.org/project/twitch-highlights/)
[![Discord](https://img.shields.io/discord/829297778324537384?color=%237289da&label=discord)](https://discord.gg/SPCj7TURj7)

An OS-independent and easy-to-use module for creating highlight videos from trending Twitch clips. Twitch highlight videos can be created by either specifying a category or a list of streamer names.  

## Getting started
### Installing
```bash
pip install twitch-highlights
```
### Import
```python
import twitch_highlights
```


## Examples
This section will describe the functions and methods provided by the package. If you would like to get started with some example code, make sure to take a look at the *examples* directory.

### TwitchHighlights
The class used to interact with the Twitch API and collect trending clips. By passing *twitch_credentials* and/or *acr_credentials* to the constructor, the proper authentication steps are performed to interact with the APIs. The object returned can be used to generate highlight videos.
```python
twitch_credentials = {
   "client_id": "1at6pyf0lvjk48san9j7fjak6hue2i",
   "client_secret": "5i2c7weuz1qmvtahrok6agi7nbqo7d"
}

acr_credentials = {
   "access_key": "m73k42t5v1jttq2h4h1r41v450lgqdpl",
   "secret_key": "1haPnq6StnU6S4FqoqzOvNAzLkapbaFeG7Pj945U",   
   "host": "identify-eu-west-1.acrcloud.com"  
}

TwitchHighlights(twitch_credentials=twitch_credentials, acr_credentials=acr_credentials)
```
Arguments:
- **twitch_credentials**: Dictionary storing the *client_id* and *client_secret* keys. Information on how to obtain these credentials can be found [here](https://dev.twitch.tv/docs/authentication#registration).
- **acr_credentials**: *(optional)* Dictionary storing the *access_key*, *secret_key* and, *host* keys. ACR is used for copyright music detection. Information on how to obtain these credentials can be found [here](https://www.acrcloud.com/music-recognition/).

### make_video_by_category
Creates a highlight video consisting of trending clip from the provided category in the current directory.
```python
highlight_generator.make_video_by_category(category = "Just Chatting", language = "en", video_length = 500)
```
Arguments:
- **category**: Name of the category from which the clips are gathered (case-insensitive).
- **output_name**: Name of the generated output mp4 file. Defaults to *"output_video"*.
- **language**: Preferred language of the clips to be included in the video. Note that the clip's language tag might not actually match the language spoken in the clip. Defaults to *None*, which means that no clips are removed.
- **video_length**: Minimum length of the video to be created in seconds. Clips are added to the combined video until this length is reached. Defaults to *300*.
- **started_at**: Starting date/time for included clips as a datetime object in the UTC standard. Defaults to exactly one day before the time at which the method is called.
- **ended_at**: Ending date/time for included clips as a datetime object in the UTC standard. Defaults to the time at which the method is called.
- **render_settings**: Dictionary containing information used for rendering and combining the clips. More information [here](#render_settings). Defaults to *None*.
- **sort_by**: Preferred ordering of clips (*"popularity", "chronologically", or "random"*). Defaults to *"popularity"*.
- **filter_copyright**: If set to True, clips containing copyrighted music are not included in the video. Defaults to False. 


### make_video_by_streamer
Creates a highlight video consisting of trending clip from the provided category in the current directory.
```python
highlight_generator.make_video_by_streamer(streamers = ["Ninja", "Myth"])
```
Arguments:
- **streamers**: List of streamer names to gather clips from.
- **output_name**: Name of the generated output mp4 file. Defaults to *"output_video"*.
- **language**: Preferred language of the clips to be included in the video. Note that the clip's language tag might not actually match the language spoken in the clip. Defaults to *None*, which means that no clips are removed.
- **video_length**: Minimum length of the video to be created in seconds. Clips are added to the combined video until this length is reached. Defaults to *300*.
- **started_at**: Starting date/time for included clips as a datetime object in the UTC standard. Defaults to exactly one day before the time at which the method is called.
- **ended_at**: Ending date/time for included clips as a datetime object in the UTC standard. Defaults to the time at which the method is called.
- **render_settings**: Dictionary containing information used for rendering and combining the clips. More information [here](#render_settings). Defaults to *None*.
- **sort_by**: Preferred ordering of clips (*"popularity", "chronologically", or "random"*). Defaults to *"popularity"*.
- **filter_copyright**: If set to True, clips containing copyrighted music are not included in the video. Defaults to False. 


### get_top_categories
Returns a list of the names of the most trending categories on Twitch at the moment of invocation. 
```python
highlight_generator.get_top_categories(5)
```
Arguments:
- **amount**: Maximum number of categories to return. Maximum: 100. Defaults to *20*.


### render_settings
Dictionary containing information used for rendering and combining the clips. When *None* is passed or if any of the keys is missing, the default values are used. 

Keys:
- **intro_path**: Path to the file containing the intro video that has to be added to the start of the generated video. If not specified, no intro is added.
- **transition_path**: Path to the file containing the transition video that has to be added between each of the clips in the generated video. If not specified, no transitions are added.
- **outro_path**: Path to the file containing the outro video that has to be added to the end of the generated video. If not specified, no outro is added.
- **target_resolution**: Tuple containing (desired_height, desired_width) to which the resolution is resized. Defaults to *(1080, 1920)*.
- **fps**: Number of frames per second. Defaults to *60*.

## License
[Apache-2.0](https://github.com/pelledrijver/twitch-highlights/blob/dev/LICENSE)

## Contributing
So far, I have been the only one who has worked on the project, and it would be great if I could get an extra pair of hands. Feel free to contact me if you have any great ideas and would like to contribute to this project. New features I'm currently working on are:
- Uploading the created video directly to YouTube
- The option to have a small animation with the name of the streamer at the start of each clip
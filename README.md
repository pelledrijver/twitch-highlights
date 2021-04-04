# twitch-highlights
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
### TwitchHighlights
The class used to interact with the Twitch API and collect trending clips. By passing *twitch_credentials* directly to the constructor, the *login_twitch* function is called automatically.
```python
highlight_generator = TwitchHighlights({
   "client_id": "1at6pyf0lvjk48san9j7fjak6hue2i",
   "client_secret": "5i2c7weuz1qmvtahrok6agi7nbqo7d"
})
```
Arguments:
- **twitch_credentials**: *(optional)* Dictionary storing the *client_id* and *client_sectet* keys.

### login_twitch
Performs the proper authentication steps using Twitch's OAuth procedure to get access to its API. This method must be called before any other methods on the TwitchHighlights object are called.

```python
highlight_generator = TwitchHighlights()
twitch_credentials = {
   "client_id": "1at6pyf0lvjk48san9j7fjak6hue2i",
   "client_secret": "5i2c7weuz1qmvtahrok6agi7nbqo7d"
}
highlight_generator.login(twitch_credentials)
```
Arguments:
- **twitch_credentials**: Dictionary storing the *client_id* and *client_sectet* keys.


### make_video_by_category
Creates a highlight video consisting of trending clip from the provided category in the current directory.
```python
highlight_generator.make_video_by_category(category = "Just Chatting", language = "en", video_length = 500)
```
Arguments:
- **category**: Name of the category from which the clips are gathered (case-insensitive).
- **output_name**: Name of the generated output mp4 file. Defaults to "*output_video*".
- **language**: Preferred language of the clips to be included in the video. Note that the clip's language tag might not actually match the language spoken in the clip. Defaults to *None*, which means that no clips are removed.
- **video_length**: Minimum length of the video to be created in seconds. Clips are added to the combined video until this length is reached. Defaults to 300.
- **started_at**: Starting date/time for included clips as a datetime object in the UTC standard. Defaults to exactly one day before the time at which the method is called.
- **ended_at**: Ending date/time for included clips as a datetime object in the UTC standard. Defaults to the time at which the method is called.
- **target_resolution**: Tuple containing (*desired_height*, *desired_width*) to which the resolution is resized. Defaults to (1080, 1920)

### make_video_by_streamer
Creates a highlight video consisting of trending clip from the provided category in the current directory.
```python
highlight_generator.make_video_by_streamer(streamers = ["Ninja", "Myth"])
```
Arguments:
- **streamers**: List of streamer names to gather clips from.
- **output_name**: Name of the generated output mp4 file. Defaults to "*output_video*".
- **language**: Preferred language of the clips to be included in the video. Note that the clip's language tag might not actually match the language spoken in the clip. Defaults to *None*, which means that no clips are removed.
- **video_length**: Minimum length of the video to be created in seconds. Clips are added to the combined video until this length is reached. Defaults to 300.
- **started_at**: Starting date/time for included clips as a datetime object in the UTC standard. Defaults to exactly one day before the time at which the method is called.
- **ended_at**: Ending date/time for included clips as a datetime object in the UTC standard. Defaults to the time at which the method is called.
- **target_resolution**: Tuple containing (*desired_height*, *desired_width*) to which the resolution is resized. Defaults to (1080, 1920)

### get_top_categories
Returns a list of the names of the most trending categories on Twitch at that moment. 
```python
highlight_generator.get_top_categories(5)
```
Arguments:
- **amount**: Maximum number of categories to return. Maximum: 100. Defaults to 20.

## License
Apache-2.0

## Contributing
So far, I have been the only one who has worked on the project and it would be great if I could get an extra pair of hands. Feel free to contact me if you have any great ideas and would like contribute to this project. New features I'm currently working on are:
- Copyright music detection
- Adding an intro/outro to the generated video
- Uploading the created video directly to YouTube
- An extra ordering feature in which the user can specify a specific ordering of clips (by number of views, chronological order, etc)

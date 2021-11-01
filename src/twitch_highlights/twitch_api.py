import requests

TWITCH_OAUTH_ENDPOINT = "https://id.twitch.tv/oauth2/token"
TWITCH_CLIPS_ENDPOINT = "https://api.twitch.tv/helix/clips"
TWITCH_CATEGORY_ENDPOINT = "https://api.twitch.tv/helix/search/categories"
TWITCH_TOP_GAMES_ENDPOINT = "https://api.twitch.tv/helix/games/top"
TWITCH_BROADCASTER_ENDPOINT = "https://api.twitch.tv/helix/users"


def login(twitch_credentials):
    twitch_client_id = twitch_credentials["client_id"]
    twitch_client_secret = twitch_credentials["client_secret"]
    query_parameters = f'?client_id={twitch_client_id}&client_secret={twitch_client_secret}&grant_type=client_credentials'

    response = requests.post(TWITCH_OAUTH_ENDPOINT + query_parameters)
    if response.status_code != 200:
        raise Exception(f'An error occured while authenticating Twitch: {response.json()["message"]}')

    twitch_token = response.json()['access_token']
    twitch_oauth_header = {"Client-ID": twitch_client_id,
                           "Authorization": f"Bearer {twitch_token}"}

    return twitch_oauth_header


def get_request(twitch_oauth_header, endpoint_url, query_parameters, error_message="An error occurred"):
    response = requests.get(endpoint_url + query_parameters, headers=twitch_oauth_header)

    if response.status_code != 200:
        raise Exception(response.json())

    if response.json()["data"] is None:
        raise Exception(error_message)

    return response.json()["data"]


def get_top_categories(twitch_oauth_header, amount=20):
    categories_json = get_request(twitch_oauth_header, TWITCH_TOP_GAMES_ENDPOINT, f"?first={amount}")
    categories = []

    for category in categories_json:
        categories.append(category['name'])

    return categories


def get_category_id(twitch_credentials, category_name):
    query_parameters = f'?query={category_name}'
    error_message = f'Twitch category not found: "{category_name}"'
    category_list = get_request(twitch_credentials, TWITCH_CATEGORY_ENDPOINT, query_parameters, error_message)
    found_category = next((category for category in category_list if category["name"].lower() == category_name.lower()),
                          None)

    if found_category is None:
        raise Exception(f'Category with name "{category_name}" not found.')

    return found_category["id"]


def get_broadcaster_id(twitch_credentials, broadcaster_name):
    query_parameters = f'?login={broadcaster_name}'
    broadcaster_data = get_request(twitch_credentials, TWITCH_BROADCASTER_ENDPOINT, query_parameters)
    if len(broadcaster_data) == 0:
        raise Exception(f'Broadcaster with name "{broadcaster_name}" not found.')

    return broadcaster_data[0]["id"]


def get_clips_by_category(twitch_credentials, category_name, started_at, ended_at):
    started_at = started_at.isoformat("T") + "Z"
    ended_at = ended_at.isoformat("T") + "Z"
    category_id = get_category_id(twitch_credentials, category_name)
    query_parameters = f'?game_id={category_id}&first=100&started_at={started_at}&ended_at={ended_at}'
    return get_request(twitch_credentials, TWITCH_CLIPS_ENDPOINT, query_parameters)


def get_clips_by_streamer(twitch_credentials, streamer_name, started_at, ended_at):
    started_at = started_at.isoformat("T") + "Z"
    ended_at = ended_at.isoformat("T") + "Z"
    broadcaster_id = get_broadcaster_id(twitch_credentials, streamer_name)
    query_parameters = f'?broadcaster_id={broadcaster_id}&first=100&started_at={started_at}&ended_at={ended_at}'

    return get_request(twitch_credentials, TWITCH_CLIPS_ENDPOINT, query_parameters)

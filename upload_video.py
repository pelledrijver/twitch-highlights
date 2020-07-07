import os
import datetime as dt
import json

def upload_video(filename, description, title):
    d = dt.datetime.utcnow() + dt.timedelta(hours=1, minutes=30)
    publishtime = d.replace(tzinfo=dt.timezone.utc).isoformat()

    metaJSON = {}
    metaJSON["title"] = title
    metaJSON["description"] = description
    metaJSON["privacyStatus"] = "private"
    metaJSON["publishAt"] = publishtime
    with open("metaJSON.json", 'w') as f:
        json.dump(metaJSON, f)


    os.system('./youtubeuploader -filename {} -metaJSON {}'.format(filename, "metaJSON.json"))

    #os.remove(filename)
    #os.remove("metaJSON.json")

def create_description(shoutouts):
    description = "Make sure to subscribe to keep up with the latest highlights! https://bit.ly/SubChug\\nWe are promoting the people in our videos and content is owned by its respective creators.\\n\\nCheck out the people in the video:\\n"
    for streamer in shoutouts:
        description+= "https://www.twitch.tv/{streamer}\\n".format(streamer)

    description+= "\\nSee a mistake in the credit list or any other problem with this video? Please email us we'll gladly help resolve the issue.\\nEmail: o102517@cygy.nl"
    return description

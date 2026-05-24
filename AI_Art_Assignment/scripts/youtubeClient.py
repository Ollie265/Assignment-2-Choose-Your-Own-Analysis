import sys
from googleapiclient.discovery import build


def youtubeClient():
    """
        Setup YouTube Data API v3 authentication.
        Replace the API key with your own.

        To obtain an API key:
        1. Go to https://console.cloud.google.com/
        2. Create a new project (or select an existing one)
        3. Enable "YouTube Data API v3"
        4. Go to Credentials -> Create Credentials -> API Key

        @returns: YouTube API service object
    """

    try:
        #
        # TODO: you specify with your own API key
        #
        apiKey = "-----------------------"

        youtube = build('youtube', 'v3', developerKey=apiKey)
    except Exception as e:
        sys.stderr.write("Failed to create YouTube client: {}\n".format(str(e)))
        sys.exit(1)

    return youtube

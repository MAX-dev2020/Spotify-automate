import spotipy
import os
import sys
import json
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

from spotipy.oauth2 import SpotifyClientCredentials

username = sys.argv[1]

try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

spotifyObject = spotipy.Spotify(auth=token)

user = spotifyObject.current_user()

print("hello")

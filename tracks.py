from logging import exception
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import json
import sys
import eyed3
# import readfiles
USERNAME = '1hja3phrnit6soklb701fpgwo'
CLIENT_ID = 'a9ead43c8e184e8dbe3520305d4dffe5'
CLIENT_SECRET = '6340f62892584212b728e211c926c2ee'
REDIRECT_URI = 'https://www.google.com/'
SCOPE = 'user-library-modify', 'playlist-modify-private', 'user-library-read', 'playlist-read-private'

token = util.prompt_for_user_token(username=USERNAME,
                                   scope=SCOPE,
                                   client_id=CLIENT_ID,
                                   client_secret=CLIENT_SECRET,
                                   redirect_uri=REDIRECT_URI)

if token:
    songname = input("Enter the track name: ")
    sp = spotipy.Spotify(auth=token)

    search_song = sp.search(q=songname.casefold(),
                            limit=1, offset=0, type='track', market=None)
    for i in range(1):
        print(json.dumps(search_song["tracks"]
                         ["items"][0]["name"], sort_keys=True, indent=4))
        print(json.dumps(search_song["tracks"]["items"][0]
                         ["artists"][0]["name"], sort_keys=True, indent=4))
"""
    print("Enter album name, if it's a single, type N0ne")
    albumname = input("Enter the album name: ")
    songname = input("Enter the track name: ")
    artistname = input("Enter artist name: ")
    wantstocreate = input(
        "Enter 0 to create a new playlist or 1 to not create a new playlist: ")

    if(wantstocreate == '0'):
        newplaylistname = input("Enter the name of your playlist: ")
    if (albumname != "N0ne"):
        search_albumid = sp.search(q=albumname.casefold(),
                                   limit=50, offset=0, type='album', market=None)

        album_id = search_albumid["albums"]["items"][0]["id"]

        album_tracks = sp.album_tracks(
            album_id, limit=50, offset=0, market=None)

        total_track = album_tracks["total"]

        limit = total_track
        for item in range(limit):
            input_songname = "".join(
                songname.split()).replace('-', '')
            songname_found = "".join(
                album_tracks["items"][item]["name"].split()).replace('-', '')
            if(input_songname.casefold() in songname_found.casefold()):
                songid = album_tracks["items"][item]["id"]
                list = [album_tracks["items"][item]["id"]]
                # print(songid)
                break
           
   # else:
      #  flag = 0
        #for i in range(50):
            # try:
        search_song = sp.search(q=songname.casefold(),
                                    limit=1, offset=0, type='track', market=None)
        # songid = search_song["tracks"]["items"][i]["id"]
        # list = [search_song["tracks"]["items"][i]["id"]]
        # if(artistname.casefold() == search_song["tracks"]["items"][i]["album"]
        # ["artists"][0]["name"]):
        # except IndexError:
        # search_song = sp.search(q=songname.casefold(),
        #  limit=3, offset=0, type='track', market=None)
        # songid = search_song["tracks"]["items"][1]["id"]
        # list = [search_song["tracks"]["items"][1]["id"]]S
        # songid = search_song["tracks"]["items"][0]["id"]
        # list = [search_song["tracks"]["items"][0]["id"]]
            # print(json.dumps(search_song["tracks"]
            # ["items"][0]["artists"][1]["name"], sort_keys=True, indent=4))
    
            for j in range(31):
                try:
                    input_artistname = "".join(
                        artistname.split()).replace('.', '')
                    artistname_found = "".join(
                        search_song["tracks"]["items"][i]["artists"][j]["name"] .split()).replace('.', '')
                    if(input_artistname.casefold() in artistname_found.casefold()):
                        songid = search_song["tracks"]["items"][i]["id"]
                        list = [search_song["tracks"]["items"][i]["id"]]

                        # print(
                        # "".join(artist_name_spaceremove .split()).replace('.', ''))
                        flag = 1
                        break
                except IndexError:
                    try:
                        songid = search_song["tracks"]["items"][i]["id"]
                    except IndexError:
                        print("Enter correct artist name")
                        sys.exit()
                    break

            if(flag == 1):
                break

        trackinfo = sp.track(songid, market=None)
        print(json.dumps(trackinfo, sort_keys=True, indent=4))
        """

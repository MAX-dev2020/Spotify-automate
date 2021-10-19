from logging import exception
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import json
import sys
import eyed3
import readfiles
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
    sp = spotipy.Spotify(auth=token)

   # searchResults = sp.search(q='roadhouse%20blues',
    #   limit=10, offset=0, type='track', market=None)
  #  limit = 10
   # for item in range(limit):
    #    artistname = searchResults["tracks"]["items"][item]["album"]["artists"][0]["name"]
    #    print(json.dumps(artistname, sort_keys=True, indent=4))
    # searchsongid = sp.search(q='new rules' + 'dua lipa',
    #                         limit=1, offset=0, type='track', market=None)
    # songid = searchsongid['tracks']['items'][0]['id']
    # list = [searchsongid['tracks']['items'][0]['id']]
   # print(json.dumps(songid, sort_keys=True, indent=4))
    # searchResults = sp.current_user_saved_tracks_add(tracks=list)

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
            if(songname.casefold() in album_tracks["items"][item]["name"].casefold()):
                songid = album_tracks["items"][item]["id"]
                list = [album_tracks["items"][item]["id"]]
                # print(songid)
                break  # song zara
    else:
        try:
            search_song = sp.search(q=songname.casefold() + artistname.casefold(),
                                    limit=50, offset=0, type='track', market=None)
            songid = search_song["tracks"]["items"][0]["id"]
            list = [search_song["tracks"]["items"][0]["id"]]
        except IndexError:
            search_song = sp.search(q=songname.casefold(),
                                    limit=50, offset=0, type='track', market=None)
            songid = search_song["tracks"]["items"][0]["id"]
            list = [search_song["tracks"]["items"][0]["id"]]

    count = 0
    numberofPlaylist = sp.current_user_playlists(limit=50, offset=0)
    for item in range(50):
        try:
            playlistName = numberofPlaylist["items"][item]["name"]
            count = count+1
        except IndexError:
            break

    print(count)

    def createPlaylist(count):
        flag = 0
        userPlaylist = sp.current_user_playlists(limit=count, offset=0)
        for item in range(count):
            playlistName = userPlaylist["items"][item]["name"]
            if(playlistName.casefold() == newplaylistname.casefold()):
                flag = 1
                print("playlist already exixts")
                return 1
        if(flag != 1):
            createplaylist = sp.user_playlist_create(
                '1hja3phrnit6soklb701fpgwo', newplaylistname, public=False, collaborative=False, description='My project')
            newplaylistid = sp.current_user_playlists(limit=1, offset=0)
            newplaylistid = newplaylistid["items"][0]["id"]
        else:
            print(json.dumps(playlistName, sort_keys=True, indent=4))

        return newplaylistid

    def addTracksToPlaylist():
        exists = 0

        if (wantstocreate == '0'):
            playlist_id = createPlaylist(count)
            if(playlist_id == 1):
                sys.exit()

        else:
            existingPlaylist = input(
                "Enter the name of the existing playlist to which the song to be added: ")
            userPlaylist = sp.current_user_playlists(limit=count, offset=0)
            for item in range(count):
                playlistName = userPlaylist["items"][item]["name"]
                if(playlistName == existingPlaylist):
                    playlist_id = userPlaylist["items"][item]["id"]
                    break
            if(item == count):
                print("playlist doesn't exixt")
                sys.exit()

        songexist = sp.playlist_tracks(
            playlist_id, fields=None, limit=100, offset=0, market=None, additional_types=('track',))
        total_plylist_tracks = songexist["total"]
        for i in range(total_plylist_tracks):
            songexistid = songexist["items"][i]["track"]["id"]
            if(songexistid == songid):
                print("song already exists")
                exists = 1
                break

        if(exists != 1):
            addTrack = sp.playlist_add_items(playlist_id, list, position=0)
            print('song added')

    addTracksToPlaylist()

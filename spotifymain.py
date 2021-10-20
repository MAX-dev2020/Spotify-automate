
# afte running the program spotify will redirect you to google.com for your permmision, grant the permission and copy the url to cmd
from posixpath import expanduser
import string
import os
from typing import Counter
import mutagen.mp3
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import json
import sys

USERNAME = ''  # enter your username
CLIENT_ID = ''  # go to spptify dev login with your account and copy client_id and Client_secert
CLIENT_SECRET = ''
REDIRECT_URI = 'https://www.google.com/'
SCOPE = 'user-library-modify', 'playlist-modify-private', 'user-library-read', 'playlist-read-private'

token = util.prompt_for_user_token(username=USERNAME,
                                   scope=SCOPE,
                                   client_id=CLIENT_ID,
                                   client_secret=CLIENT_SECRET,
                                   redirect_uri=REDIRECT_URI)


if token:
    sp = spotipy.Spotify(auth=token)
    hint = 0
    created = 0
    offset = 0
    stopp = False
    songexistlist = []
    albumnotfound = False

    wantstocreate = input(
        "Enter 0 to create a new playlist or 1 to insert songs into existing playlist: ")

    if(wantstocreate == '0'):
        newplaylistname = input("Enter the name of your playlist: ")

    else:
        existingPlaylist = input(
            "Enter the name of the existing playlist: ")
    # enter your destination path of your msuic folder
    for root, dirs, files in os.walk('E:/Music'):
        for file in files:

            filename, extension = os.path.splitext(file)
            if (extension == '.mp3'):
                try:
                    # enter your destination path of your msuic folder
                    audio = EasyID3("E:/Music/{0}.mp3".format(filename))
                except ID3NoHeaderError:
                    continue

                if 'album' in audio:
                    albumname = audio['album'][0]

                if 'title' in audio:
                    songname = audio['title'][0]
                    if(songname == ''):
                        continue

                if 'artist' in audio:
                    artistname = audio['artist'][0]
                    if(',' in artistname[0]):
                        newlist_artist = []
                        for string in artistname:
                            for item in string.split(','):
                                newlist_artist.append(item.strip())
                                artistname = newlist_artist[0]

                limitcount = 0
                limit = 0
                if(albumname != ''):
                    albumhyphen = albumname
                    if('-' in albumhyphen):
                        albumhyphen = albumhyphen.split("-", 1)

                        albumname = albumhyphen[0]
                    if('[' in albumhyphen):
                        albumname = albumhyphen.split("[", 1)

                        albumname = albumhyphen[0]

                    search_albumid = sp.search(q=albumname.casefold(),
                                               limit=50, offset=0, type='album', market=None)
                    try:
                        album_id = search_albumid["albums"]["items"][0]["id"]
                    except IndexError:
                        albumnotfound = True
                        print("album not found")

                    if(albumnotfound != True):
                        album_tracks = sp.album_tracks(
                            album_id, limit=50, offset=0, market=None)

                        total_track = album_tracks["total"]

                        limit = total_track

                        for item in range(limit):
                            try:
                                input_songname = "".join(
                                    songname.split()).replace('-', '')
                            except NameError:
                                stopp = True
                                break
                            songname_found = "".join(
                                album_tracks["items"][item]["name"].split()).replace('-', '')
                            if(input_songname.casefold() == songname_found.casefold()):
                                songid = album_tracks["items"][item]["id"]
                                list = [album_tracks["items"][item]["id"]]

                                break
                            limitcount = limitcount+1

                songnames = True
                artistnames = True

                if(limitcount == limit or albumnotfound == True):
                    songcount = 0
                    flag = 0
                    print("songs name enteres")
                    for i in range(10):

                        try:
                            songhyphen = songname
                            if('-' in songhyphen):
                                songhyphen = songhyphen.split("-", 1)

                                songname = songhyphen[0]
                            if('[' in songhyphen):
                                songname = songhyphen.split("[", 1)

                                songname = songhyphen[0]
                                if(songname != ''):
                                    search_song = sp.search(q=songname.casefold(),
                                                            limit=10, offset=0, type='track', market=None)

                        except NameError:

                            break

                        for j in range(31):
                            try:
                                input_artistname = "".join(
                                    artistname.split()).replace('.', '')
                                artistname_found = "".join(
                                    search_song["tracks"]["items"][i]["artists"][j]["name"] .split()).replace('.', '')
                                if(input_artistname.casefold() in artistname_found.casefold()):
                                    songid = search_song["tracks"]["items"][i]["id"]
                                    list = [search_song["tracks"]
                                            ["items"][i]["id"]]

                                    flag = 1
                                    break
                            except IndexError:
                                artistnames = False
                                flag = 1
                                break

                        if(flag == 1):
                            break
                        songcount = songcount+1

                    if(songname != ''):
                        try:
                            search_song = sp.search(q=songname.casefold(),
                                                    limit=1, offset=0, type='track', market=None)
                            songid = search_song["tracks"]["items"][0]["id"]
                            list = [search_song["tracks"]["items"][0]["id"]]

                            print(json.dumps(
                                search_song["tracks"]["items"][0]["name"], sort_keys=True, indent=4))
                            print(json.dumps(
                                [search_song["tracks"]["items"][0]["id"]], sort_keys=True, indent=4))
                        except NameError:
                            continue
                        except IndexError:
                            continue

                numberofPlaylist = sp.current_user_playlists(
                    limit=50, offset=0)
                count = 0
                for item in range(50):
                    try:
                        playlistName = numberofPlaylist["items"][item]["name"]
                        count = count+1
                    except IndexError:
                        break

                print(count)

                def createPlaylist(count):

                    flag = 0
                    userPlaylist = sp.current_user_playlists(
                        limit=count, offset=0)
                    for item in range(count):
                        playlistName = userPlaylist["items"][item]["name"]
                        if(playlistName.casefold() == newplaylistname.casefold()):
                            flag = 1
                            print("playlist already exixts")
                            return 1
                    if(flag != 1):
                        createplaylist = sp.user_playlist_create(
                            '1hja3phrnit6soklb701fpgwo', newplaylistname, public=False, collaborative=False, description='My project')
                        newplaylistid = sp.current_user_playlists(
                            limit=1, offset=0)
                        newplaylistid = newplaylistid["items"][0]["id"]
                    else:
                        print(json.dumps(playlistName, sort_keys=True, indent=4))

                    return newplaylistid

                def addTracksToPlaylist(count):
                    exists = 0
                    global created

                    if (wantstocreate == '0' and created == 0):
                        playlist_id = createPlaylist(count)
                        global existingPlaylist
                        created = 1
                        existingPlaylist = newplaylistname
                        if(playlist_id == 1):
                            sys.exit()

                    else:
                        userPlaylist = sp.current_user_playlists(
                            limit=count, offset=0)
                        for item in range(count):
                            playlistName = userPlaylist["items"][item]["name"]

                            if(playlistName == existingPlaylist):
                                try:
                                    playlist_id = userPlaylist["items"][item]["id"]
                                    break
                                except UnboundLocalError:
                                    print("playlist doesn't exixt")
                                    sys.exit()

                    results = sp.user_playlist_tracks(
                        'zdejs0clebnjaz00zu91k1mrk', playlist_id)
                    tracks = results['items']
                    totaltracks = 0
                    while results['next']:
                        results = sp.next(results)
                        tracks.extend(results['items'])

                    for i in tracks:
                        totaltracks = totaltracks + 1

                    for i in range(totaltracks):
                        try:
                            existingtrack = tracks[i]["track"]["id"]
                            if(existingtrack == songid):
                                print("song already exists")
                                exists = 1
                                break
                        except IndexError:
                            return True
                        except NameError:
                            return True
                    print(playlist_id)
                    try:
                        if(exists != 1):
                            addTrack = sp.playlist_add_items(
                                playlist_id, list, position=0)
                            print('song added')
                            return True
                    except TypeError:
                        return True
                    return True

                if(addTracksToPlaylist(count) == True):
                    continue

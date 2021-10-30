
# after running the program spotify will redirect you to google.com for your permmision, grant the permission and copy the url to cmd
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
import re

# "https://www.spotify.com/us/account/overview/" copy your username and paste it here
USERNAME = ''
# go to "https://developer.spotify.com/",  login with your spotify account and copy your client_id and client_secert and paste it here
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'https://www.google.com/'
SCOPE = 'user-library-modify', 'playlist-modify-private', 'user-library-read', 'playlist-read-private'

token = util.prompt_for_user_token(username=USERNAME,
                                   scope=SCOPE,
                                   client_id=CLIENT_ID,
                                   client_secret=CLIENT_SECRET,
                                   redirect_uri=REDIRECT_URI)

notadded = []
if token:
    sp = spotipy.Spotify(auth=token)
    hint = 0
    created = 0
    offset = 0
    id3error = 0
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
    # enter your destination path of your music folder
    for root, dirs, files in os.walk('E:/Music'):
        for file in files:
            filename, extension = os.path.splitext(file)
            if (extension == '.mp3'):
                try:
                    # enter your destination path of your music folder
                    audio = EasyID3("E:/Music/{0}.mp3".format(filename))
                except ID3NoHeaderError:
                    id3error += 1
                    continue

                if 'album' in audio:
                    albumname = audio['album'][0]

                if 'title' in audio:
                    songlist = audio['title'][0]
                    songextrachar = songlist
                    if(songlist == ''):
                        notadded.append(albumname)
                        continue

                if 'artist' in audio:
                    artistnames = audio['artist'][0]
                    if(',' in artistnames[0]):
                        newlist_artist = []
                        for string in artistname:
                            for item in string.split(','):
                                newlist_artist.append(item.strip())
                                artistname = newlist_artist[0]

                limitcount = 0
                limit = 0
                try:
                    for i in range(3):
                        try:
                            if('[' in songlist):
                                pattern = re.search(r'\[', songlist)
                                pattern2 = re.search(r']', songlist)
                                songlist = songlist[:pattern.span()[0]] + \
                                    songlist[pattern2.span()[1]:]
                            if('(' in songlist):
                                pattern = re.search(r'\(', songlist)
                                pattern2 = re.search(r'\)', songlist)
                                songlist = songlist[:pattern.span()[0]] + \
                                    songlist[pattern2.span()[1]:]

                        except AttributeError:
                            continue
                    if('|' in songlist):
                        songextrachar = songlist.split("|", 1)

                        songlist = songextrachar[0]
                    if('(' in songlist):
                        songextrachar = songlist.split(
                            "(                        ", 1)

                        songlist = songextrachar[0]
                    if('[' in songlist):
                        songextrachar = songlist.split("[", 1)

                        songlist = songextrachar[0]
                    if('-' in songlist):
                        songextrachar = songlist.split("-", 1)
                        ans = bool(re.search(r'\d', songextrachar[0]))
                        if (ans == False):
                            songlist = songextrachar[0]
                        else:
                            songlist = songextrachar[1]
                    if('.' in songlist):
                        songextrachar = songlist.split(".", 1)

                        songlist = songextrachar[0]
                    try:
                        pattern = re.search(r'[^a-zA-Z0-9 ]', songlist)
                        songlist = songlist[:pattern.span()[0]] + \
                            songlist[pattern.span()[1]:]
                    except AttributeError:
                        pass

                    songname = songlist
                    # print(songlist)
                    if 'artist' in audio:
                        artistnames = audio['artist']
                    # print(audio['artist'])

                    if(',' in artistnames[0]):
                        for string in artistnames:
                            for item in string.split(','):
                                newlist_artist.append(item.strip())
                                artistnames = newlist_artist[0]
                        # print(artistname)
                        # continue

                    artistname = artistnames[0]
                    for i in range(3):
                        try:
                            if('[' in artistname):
                                pattern = re.search(r'\[', artistname)
                                pattern2 = re.search(r']', artistname)
                                artistname = artistname[:pattern.span()[0]] + \
                                    artistname[pattern2.span()[1]:]
                            if('(' in songlist):
                                pattern = re.search(r'\(', artistname)
                                pattern2 = re.search(r'\)', artistname)
                                artistname = artistname[:pattern.span()[0]] + \
                                    artistname[pattern2.span()[1]:]

                        except AttributeError:
                            continue
                    if('|' in artistname):
                        artistextrachar = artistname.split("|", 1)

                        artistname = artistextrachar[0]
                    if('(' in artistname):
                        artistextrachar = artistname.split("(", 1)

                        artistname = artistextrachar[0]
                    if('[' in artistname):
                        artistextrachar = artistname.split("[", 1)

                        artistnamet = artistextrachar[0]
                    if('-' in artistname):
                        artistextrachar = artistname.split("-", 1)
                        ans = bool(re.search(r'\d', artistextrachar[0]))
                        if (ans == False):
                            artistname = artistextrachar[0]
                        else:
                            artistname = artistextrachar[1]
                    if('.' in artistname):
                        artistextrachar = artistname.split('.', 1)
                        artistname = artistextrachar[1]

                    try:
                        pattern = re.search(r'[^a-zA-Z0-9 ]', artistname)
                        artistname = artistname[:pattern.span()[0]] + \
                            artistname[pattern.span()[1]:]
                    except AttributeError:
                        pass

                except NameError:
                    continue
                except TypeError:
                    continue

                if(limitcount == limit or albumnotfound == True):
                    songcount = 0
                    flag = 0
                    print("songs name enteres")
                    for i in range(10):

                        try:
                            if(songname != ''):
                                search_song = sp.search(q=songname.casefold(),
                                                        limit=10, offset=0, type='track', market=None)
                        except NameError:

                            break

                        for j in range(31):
                            try:
                                input_artistname = artistname
                                artistname_found = search_song["tracks"]["items"][i]["artists"][j]["name"]

                                if(input_artistname.casefold() in artistname_found.casefold()):
                                    songid = search_song["tracks"]["items"][i]["id"]
                                    list = [search_song["tracks"]
                                            ["items"][i]["id"]]

                                    flag = 1
                                    break
                            except IndexError:
                                artistnames = False
                                break
                            except NameError:
                                artistnames = False
                                break

                        if(flag == 1):
                            break
                        songcount = songcount+1

                    if(songcount == 10):
                        try:
                            if(songname != ''):
                                search_song = sp.search(q=songname.casefold(),
                                                        limit=1, offset=0, type='track', market=None)
                                songid = search_song["tracks"]["items"][0]["id"]
                                list = [search_song["tracks"]
                                        ["items"][0]["id"]]

                                print(json.dumps(
                                    search_song["tracks"]["items"][0]["name"], sort_keys=True, indent=4))
                                print(json.dumps(
                                    [search_song["tracks"]["items"][0]["id"]], sort_keys=True, indent=4))
                        except NameError:
                            notadded.append(songname)
                            continue
                        except IndexError:
                            notadded.append(songname)
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
                            USERNAME, newplaylistname, public=False, collaborative=False, description='My project')
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
                        USERNAME, playlist_id)
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
                            return
                        else:
                            notadded.append(songname)
                            return
                    except TypeError:
                        return True
                    except NameError:
                        return True

                if(addTracksToPlaylist(count) == True):
                    continue
print("\n")
print("songs that were not added")
for i in range(len(notadded)):
    print(notadded[i])

print(id3error, "song errors")


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
    sp = spotipy.Spotify(auth=token)  # gets the access token
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
    # this for loop goes through the directorys which leads to your music folder
    for root, dirs, files in os.walk('E:/Music'):
        for file in files:
            # gets the extenions of the .mp3 file
            filename, extension = os.path.splitext(file)
            if (extension == '.mp3'):  # checks if its .mp3 file
                try:
                    # enter your destination path of your music folder
                    # id3 is a container which stores all the meta data of the music file
                    audio = EasyID3("E:/Music/{0}.mp3".format(filename))
                # throws exception when the song doesn't contain ID3 tag which contains the metadara
                except ID3NoHeaderError:

                    continue

                if 'album' in audio:                         # checks if the files contains album name
                    # if the condition is true then it gets the album name
                    albumname = audio['album'][0]

                if 'title' in audio:                         # checks if the files contains title name
                    # if the condition is true then it gets the title name
                    songlist = audio['title'][0]
                    songextrachar = songlist
                else:
                    continue

                if 'artist' in audio:                        # checks if the files contains artist name
                    # if the condition is true then it gets the artist name
                    artistnames = audio['artist']
                    # this condition is to find if there are more than one artists by checking if theres a comma in the string
                    if(',' in artistnames[0]):
                        newlist_artist = []
                        for string in artistnames:           # if theres a comma it means there are more than one artists so this splits the string
                            # and adds the artistname into a list
                            for item in string.split(','):
                                newlist_artist.append(item.strip())
                                artistnames = newlist_artist

                    artistname = '-'.join(artistnames)
                    artistname = ' '.join(artistnames)

                else:
                    continue
# # # # # # # # # #  code from 96 to 262 removes any characters like '.',',','[',']' or '(' other othan words and removes unwanted strings in the title and artist name #  # # # # # # # # # #
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
                        # splits the string between  '|'
                        songextrachar = songlist.split("|", 1)

                        # selects the first part of the string
                        songlist = songextrachar[0]
                    if('(' in songlist):
                        songextrachar = songlist.split(
                            "(", 1)  # splits the string between  '('

                        # selects the first part of the string
                        songlist = songextrachar[0]
                    if('[' in songlist):
                        # splits the string between  '['
                        songextrachar = songlist.split("[", 1)

                        # selects the first part of the string
                        songlist = songextrachar[0]
                    if('-' in songlist):
                        # splits the string between  ']'
                        songextrachar = songlist.split("-", 1)
                        # checks if there's a number in the song name
                        ans = bool(re.search(r'\d', songextrachar[0]))
                        if (ans == False and songextrachar[0] != ''):
                            # selects the first part of the string
                            songlist = songextrachar[0]
                        else:
                            # selects the second part of the string
                            songlist = songextrachar[1]

                    print(songlist)

                    if("ft." in songlist):
                        print("true")
                        songlist = songlist .replace('ft', '')

                        print(songlist, "replaced")

                    if("Ft." in songlist):
                        print("true")
                        songlist = songlist .replace('Ft', '')

                        print(songlist, "replaced")

                    if("feat." in songlist):
                        print("true")
                        songlist = songlist .replace('feat', '')

                        print(songlist, "replaced")

                    if("Feat." in songlist):
                        print("true")
                        songlist = songlist .replace('Feat', '')
                        print(songlist, "replaced")

                    if('.' in songlist):
                        songlist = songlist.replace('.', ' ')

                    if(':' in songlist):

                        songextrachar = songlist.split(":", 1)

                        songlist = songextrachar[0]

                    songname = songlist
                    # print(songlist)

                    # print(artistname)
                    # continue

                    # this part for the code works just like the song name

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

                        artistname = artistextrachar[0]
                    if('-' in artistname):
                        artistextrachar = artistname.split("-", 1)
                        ans = bool(re.search(r'\d', artistextrachar[0]))
                        if (ans == False):
                            artistname = artistextrachar[0]
                        else:
                            artistname = artistextrachar[1]

                    if("ft." in artistname):
                        print("true")
                        artistname = artistname.replace('ft', '')
                        print(artistname, "replaced")

                    if("Ft." in artistname):
                        print("true")
                        artistname = artistname.replace('Ft', '')
                        print(artistname, "replaced")

                    if("feat." in artistname):
                        print("true")
                        artistname = artistname.replace('feat', '')
                        print(artistname, "replaced")

                    if("Feat." in artistname):
                        print("true")
                        artistname = artistname.replace('Feat', '')
                        print(artistname, "replaced")

                    if('.' in artistname):
                        artistname = artistname.replace('.', ' ')

                    if(':' in artistname):
                        artistextrachar = artistname.split(":", 1)

                        artistname = artistextrachar[0]

                    try:
                        # searches for  charactes other than alphabets, numbers and whitespace
                        pattern = re.search(r'[&]', artistname)
                        artistname = artistname[:pattern.span()[0]] + \
                            artistname[pattern.span()[1]:]
                    except AttributeError:
                        pass

                except NameError:
                    continue
                except TypeError:
                    pass
# # # # # # # # # # # # # # # # # # # # # # # # # # #  # # # # # # # # # # # # # # # # # # # # # # # # # #  # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # #  264 to 328 is the searching algorithm which searches for the songs accurately and fetches the song id  # # # # # # # # # # # # # # # # # # # # # # # # # #
                print(artistname)
                print(songname)
                songcount = 0
                flag = 0
                songnotfound = 0
                done = 1
                print("songs name enteres")
                for i in range(10):

                    try:
                        if(songname != '' and artistname != ''):
                            search_song = sp.search(q='artist:' + artistname + ' track:' + songname, limit=10,
                                                    type='track', market=None)  # "search" API reference gets the song name
                    except NameError:

                        break

                    try:
                        for j in range(len(search_song["tracks"]["items"][i]["artists"])):
                            if (search_song["tracks"]["items"][i]["artists"][j]["name"].casefold() in artistname.casefold()):
                                songnotfound = 0
                                if (songnotfound == 0):
                                    songid = search_song["tracks"]["items"][i]["id"]
                                    list = [search_song["tracks"]
                                            ["items"][i]["id"]]

                                    done = 0

                            else:
                                songnotfound = 1
                                done = 1

                        if (done == 0):
                            break
                        else:
                            continue

                    except IndexError:
                        songnotfound = 1
                        break

                # if theres no proper artist name, then this algo searches  for the song using only song name
                if(artistname == '' or songnotfound == 1):
                    songnotfound = 0
                    print("enter search song")
                    try:
                        if(songname != ''):
                            search_song = sp.search(q=songname.casefold(),  # searches the song
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
#  # # # # # # # # # # # # # # # # # # # # # # # # # #  # # # # # # # # # # # # # # # # # # # # # # # # # #  # # # # # # # # # # # # # # # # # # # # # # # # # #
                numberofPlaylist = sp.current_user_playlists(
                    limit=50, offset=0)                        # gets the total number of user playlists
                count = 0
                for item in range(50):
                    try:
                        playlistName = numberofPlaylist["items"][item]["name"]
                        # this for loop is a counter which gets the total number of user playlists
                        count = count+1
                    except IndexError:
                        break

                print(count)

 # # # # # # # # # # # # # # # # # # # # # # # # The function  createPlaylist creates a new playlist # # # #  # # # # # # # # # # # # # # # # # # # # # # # # # #

                def createPlaylist(count):

                    flag = 0
                    userPlaylist = sp.current_user_playlists(
                        limit=count, offset=0)   # gets the user playlists
                    for item in range(count):
                        playlistName = userPlaylist["items"][item]["name"]
                        # checks if  there's a playlist with the same name or not
                        if(playlistName.casefold() == newplaylistname.casefold()):
                            flag = 1
                            # if its true then it returns 1
                            print("playlist already exixts")
                            return 1
                    if(flag != 1):
                        createplaylist = sp.user_playlist_create(
                            USERNAME, newplaylistname, public=False, collaborative=False, description='My project')  # if there's no playlist with the same name it creates a new playlist
                        newplaylistid = sp.current_user_playlists(
                            limit=1, offset=0)  # gets the playlsit id
                        newplaylistid = newplaylistid["items"][0]["id"]
                    else:
                        print(json.dumps(playlistName, sort_keys=True, indent=4))

                    return newplaylistid

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

 # # # # # # # # # # # # # # # the function addTracksToPlaylist adds songs to the user playlist # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

                def addTracksToPlaylist(count):
                    exists = 0
                    global created

                    # checks if user wants to create a new playlist or not
                    if (wantstocreate == '0' and created == 0):
                        # if its true then it calls the function createPlaylist
                        playlist_id = createPlaylist(count)
                        global existingPlaylist
                        created = 1  # if the new playlist is created then the variable created is equal to 1
                        existingPlaylist = newplaylistname
                        # if the playlist already exits with the same name then the program stops with a message
                        if(playlist_id == 1):
                            sys.exit()

                    else:
                        userPlaylist = sp.current_user_playlists(
                            limit=count, offset=0)  # is the doesn't wants to create a new playlist then gets the user current playlsits
                        for item in range(count):
                            playlistName = userPlaylist["items"][item]["name"]

                            # checks if the  name of the playlist given by the user is same as the name of the existing playlist
                            if(playlistName == existingPlaylist):
                                try:
                                    playlist_id = userPlaylist["items"][item]["id"]
                                    break
                                except UnboundLocalError:
                                    print("playlist doesn't exixt")
                                    sys.exit()
                    try:
                        # gets all the tracks in the user playlist
                        results = sp.user_playlist_tracks(
                            USERNAME, playlist_id)
                    except UnboundLocalError:
                        print("playlist doesn't exixt")
                        sys.exit()

                    tracks = results['items']
                    totaltracks = 0
                    while results['next']:
                        # gets the name of all the tracks in the user playlist
                        results = sp.next(results)
                        tracks.extend(results['items'])

                    for i in tracks:
                        totaltracks = totaltracks + 1

                    for i in range(totaltracks):
                        try:
                            existingtrack = tracks[i]["track"]["id"]
                            # checks if the song  exists in the playlist or not
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
                        # if the song doesn't alreay exists in the playlsit then it adds the song
                        if(exists != 1):
                            addTrack = sp.playlist_add_items(  # adds the song to the playlist
                                playlist_id, list, position=0)
                            print('song added')
                            return
                    except TypeError:
                        return True
                    except NameError:
                        return True

                if(addTracksToPlaylist(count) == True):
                    continue

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#

print(id3error, "Id3 errors")
# print("\n")
# print("songs that were not added")  # prints the songs that were not added
# for i in range(len(notadded)):
#     print(notadded[i])

# print(id3error, "song errors")

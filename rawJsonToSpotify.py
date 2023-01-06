
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
USERNAME = ''
CLIENT_ID = ''
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
    # enter your destination path of your music folder
    with open('raw.json') as f:
        data = json.load(f)
    listSongs = []
    for i in data['songs']:
        listSongs.append(({'song': i['song'],'album': i['album'], 'singers': i['singers'],'music': i['music'], 'year': i['year']}))
    for i in listSongs:
        print(i)
    count = 0
    #search for the song in spotify
    for i in listSongs:
        if(count < 415):
            if(wantstocreate == '0'):
                if(created == 0):
                    playlist = sp.user_playlist_create(
                        USERNAME, newplaylistname, public=False)
                    created = 1
            else:
                playlists = sp.user_playlists(USERNAME)
                for playlist in playlists['items']:
                    if playlist['name'] == existingPlaylist:
                        break
            song = i['song']
            album = i['album']
            singers = i['singers']
            music = i['music']
            year = i['year']
            print("Searching for: " + song + " by " + singers)
            results = sp.search(q='track:' + song + ' artist:' + singers, type='track')
            items = results['tracks']['items']
            if len(items) > 0:
                track = items[0]
                print("Found: " + track['name'] + " by " + track['artists'][0]['name'])
                songexistlist.append(track['id'])
                count += 1
            else:
                print("Song not found in spotify")
                albumnotfound = True
                hint = 1
            
    print('songexistlist', songexistlist)
    print(len(songexistlist))
    # remove 1 to 100 songs from the songexistlist
    c = 0
    songexistlist.reverse()
    for k in range(len(songexistlist)):
        if c == 300:
            break
        songexistlist.pop()
        c += 1
    print('songexistlist', songexistlist)
    if(wantstocreate == '0'):
            sp.user_playlist_add_tracks(USERNAME, playlist['id'], songexistlist)
    else:
        sp.user_playlist_add_tracks(USERNAME, playlist['id'], songexistlist)
        print("Songs added to playlist")
else:
    print("Can't get token for", USERNAME)







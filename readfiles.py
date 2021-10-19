import string
import os
from typing import Counter
import mutagen.mp3
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError
# audio = MP3("E:/Music/")
# print(f)
count = 0
list = []
artistlist = []
albumlist = []
songlist = []
newlist = []
for root, dirs, files in os.walk('E:/Music'):
    for file in files:

        filename, extension = os.path.splitext(file)
        if (extension == '.mp3'):
            try:
                audio = EasyID3("E:/Music/{0}.mp3".format(filename))
            except ID3NoHeaderError:
                continue
            """
            if 'album' in audio:
                albumlist.append(audio['album'])
                # print(audio['album'])
            if 'title' in audio:
                songlist.append(audio['title'])

            # print(audio['title'])
            if 'artist' in audio:
                artistlist.append(audio['artist'])
        """
            # print(filename)
            # songname = '{0}.mp3'.format(filename)
            # list.append(filename.encode("utf-8"))
            # list.append(audio)
            if 'album' in audio:
                albumlist = audio['album'][0]
                # print(audio['album'])
            if 'title' in audio:
                songlist = audio['title'][0]
                print(audio['title'])
            if 'artist' in audio:
                artistname = audio['artist']
                # print(audio['artist'])

                if(',' in artistname[0]):
                    newlist_artist = []
                    for string in artistname:
                        for item in string.split(','):
                            newlist_artist.append(item.strip())
                            artistname = newlist_artist[0]
                    print(artistname)
                    continue

                print(artistname[0])

                count = count+1
                """

# print(count)
# print(list)
# print(len(list))
count = 0
for item in range(len(songlist)):
    print(songlist[item])
    count = count + 1
    print(count)
# print(artistlist[count - 3])
# print(songlist[count - 16])
# artistname = artistlist[count - 3][0]
# ongname = songlist[count - 16][0]
"""

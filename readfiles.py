import string
import os
import mutagen.mp3
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError
# audio = MP3("E:/Music/")
# print(f)
count = 0
list = []
for root, dirs, files in os.walk('E:/Music'):
    for file in files:
        filename, extension = os.path.splitext(file)
        if (extension == '.mp3'):
            audio = EasyID3("E:/Music/{0}.mp3".format(filename))
            # print(filename)
            #songname = '{0}.mp3'.format(filename)
            list.append(filename.encode("utf-8"))
        if 'album' in audio:
            print(audio['album'])
# print(list)
# print(len(list))

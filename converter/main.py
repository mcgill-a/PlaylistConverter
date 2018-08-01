import random
import sys
import os
import eyed3


print("Playlist Converter")

main_directory = "E:\A\Music"
music_library = "E:\A\Music\Library"

playlist_directory = "E:\A\Music\_python\Playlists\Forgetable"
playlist_in = "E:\A\Music\_python\Playlists\Forgetable\playlist.m3u"
playlist_out = "E:\A\Music\_python-playlists"

playlist_file = open(playlist_in, "r")

index = 0;
for line in playlist_file:
    #print(index," ", line)
    index += 1

    file_path = playlist_directory + "\\" + line
    file_path = file_path.rstrip()
    #print(file_path)

    audiofile = eyed3.load(file_path)
    artists = audiofile.tag.artist
    artists = artists.split(',')
    primary_artist = artists[0]

    real_location = music_library + "\\" + primary_artist + "\\" + audiofile.tag.album + "\\" + line
    print(real_location)
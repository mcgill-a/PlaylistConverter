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

songs = []

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
    #print(real_location)
    songs.append(real_location)

playlist_file.close()

name = "Forgetable.m3u"
full_name = playlist_out + "\\" + name
playlist_file_out = open(full_name, "w")
playlist_file_out.write("# Converted with Playlist Converter by Alex McGill\n")
playlist_file_out.write("# " + name + "\n")
playlist_file_out.writelines(songs)
playlist_file_out.close()
#for current in songs:
    #print(current)
    #current.rstrip()
    #playlist_file_out.write

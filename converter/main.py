import random
import sys
import os
import eyed3


print("Playlist Converter")

main_directory = "E:\A\Music"
music_library = "E:\A\Music\Library"

#playlist_directory = "E:\A\Music\_python\Playlists\Forgetable"
#playlist_in = "E:\A\Music\_python\Playlists\Forgetable\playlist.m3u"

playlist_in = input("Please enter the absolute path of the playlist file\n")
while not os.path.exists(playlist_in):
    playlist_in = input("Playlist file does not exist, please try again\n")

playlist_directory = os.path.dirname(playlist_in)

name = input("Please enter a name for the converted playlist: ")
while len(name) < 1:
    name = input("Invalid name. Please enter a valid name: ")

# Reverse the filename to check whether it has a .m3u extension
# If length is not more than 4 then it physically cannot have a .m3u extension
if len(name) > 4:
    reversed = name[::-1]
    reversed = reversed[0:4]
    reversed = reversed[::-1]

# If the filename does not include .m3u then add it
if not reversed == ".m3u":
    name += ".m3u"

playlist_out = "E:\A\Music\_python-playlists"

playlist_file = open(playlist_in, "r")

songs = []

index = 0;
for line in playlist_file:
    #print(index," ", line)
    index += 1

    file_path = playlist_directory + "\\" + line
    file_path = file_path.rstrip()
    print(file_path)

    audiofile = eyed3.load(file_path)
    artists = audiofile.tag.artist
    artists = artists.split(',')
    primary_artist = artists[0]
    album = audiofile.tag.album

    real_location = music_library + "\\" + primary_artist + "\\" + album + "\\" + line
    #print(real_location)
    if len(primary_artist) > 0 and len(album) > 0:
        songs.append(real_location)
    else:
        print("Failed to convert: " + file_path)

playlist_file.close()

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

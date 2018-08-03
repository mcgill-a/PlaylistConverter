import random
import sys
import os
import eyed3

print("------------------ Playlist Converter ------------------")

main_directory = "E:\A\Music"
music_library = "E:\A\Music\Library"
playlist_in = ""
playlist_name = ""


def request_playlist():
    playlist = input("Please enter the absolute path of the playlist file:\n")
    extension = ""
    if len(playlist) > 4:
        extension = get_extension(playlist)
    while not os.path.isfile(playlist) or extension != ".m3u":
        if len(playlist) > 4:
            extension = get_extension(playlist)

        if playlist.upper() == "EXIT":
            print("Program shutdown")
            sys.exit(0)
        elif os.path.isdir(playlist):
            playlist = input("'" + playlist + "' is a directory not a file, please try again:\n")
        elif not os.path.isfile(playlist):
            playlist = input("File does not exist, please try again:\n")
        elif not extension == ".m3u":
            playlist = input("File is not of type M3U [playlist.m3u], please try again:\n")
    print("Playlist file was found! Importing " + playlist)
    return playlist;


def get_extension(input):

    # Reverse the filename to check whether it has a .m3u extension
    # If length is not more than 4 then it physically cannot have a .m3u extension
    rev = ""
    if len(input) > 4:
        rev = input[::-1]
        rev = rev[0:4]
        rev = rev[::-1]
    return rev;


def request_output_name():
    name = input("Please enter a name for the converted playlist: ")
    while len(name) < 1:
        name = input("Invalid name. Please enter a valid name: ")

    # If the chosen filename does not include .m3u then add it
    if get_extension(name) != ".m3u":
        name += ".m3u"
    return name;


playlist_output_dir = "E:\A\Music\_python-playlists"

playlist_in = request_playlist()
playlist_name = request_output_name()

playlist_file = open(playlist_in, "r")

songs = []

success_count = 0;
fail_count = 0;

for line in playlist_file:

    file_path = os.path.dirname(playlist_in) + "\\" + line
    file_path = file_path.rstrip()

    if os.path.exists(file_path):
        audiofile = eyed3.load(file_path)
        artists = ""
        if audiofile.tag.artist is not None:
            artists = audiofile.tag.artist
        artists = artists.split(',')
        primary_artist = artists[0]
        album = ""
        if audiofile.tag.album is not None:
            album = audiofile.tag.album

        real_location = music_library + "\\" + primary_artist + "\\" + album + "\\" + line

        if not os.path.isfile(real_location.rstrip()):
            print("Warning: " + real_location.rstrip() + " does not exist in music library")
        else:
            if len(primary_artist) > 0 and len(album) > 0:
                songs.append(real_location)
                success_count += 1
            else:
                print("Failed to convert: " + file_path)
                fail_count += 1
    else:
        print("Failed to convert: " + file_path)
        fail_count += 1

playlist_file.close()

full_name = playlist_output_dir + "\\" + playlist_name
playlist_file_out = open(full_name, "w", encoding='utf-8')
playlist_file_out.write("# Converted with Playlist Converter by Alex McGill\n")
playlist_file_out.write("# " + playlist_name + "\n")
playlist_file_out.writelines(songs)
playlist_file_out.close()

# Display conversion results
print(success_count, "songs successfully converted")
if fail_count == 1:
    print(fail_count, "song failed to convert")
elif fail_count > 1:
    print(fail_count, "songs failed to convert")
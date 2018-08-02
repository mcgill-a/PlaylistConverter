import random
import sys
import os
import eyed3


print("Playlist Converter")

main_directory = "E:\A\Music"
music_library = "E:\A\Music\Library"
playlist_in = ""
playlist_name = ""


def requestPlaylist():
    playlist = input("Please enter the absolute path of the playlist file\n")
    while not os.path.exists(playlist):
        if playlist.upper() == "EXIT":
            print("Program shutdown")
            sys.exit(0)
        playlist = input("Playlist file does not exist, please try again\n")
    return playlist;

#playlist_directory = os.path.dirname(playlist_in)

def requestOutputName():
    name = input("Please enter a name for the converted playlist: ")
    while len(name) < 1:
        name = input("Invalid name. Please enter a valid name: ")

    # Reverse the filename to check whether it has a .m3u extension
    # If length is not more than 4 then it physically cannot have a .m3u extension
    reversed = ""
    if len(name) > 4:
        reversed = name[::-1]
        reversed = reversed[0:4]
        reversed = reversed[::-1]

    # If the chosen filename does not include .m3u then add it
    if not reversed == ".m3u":
        name += ".m3u"
    return name;

playlist_output_dir = "E:\A\Music\_python-playlists"

playlist_in = requestPlaylist()
playlist_name = requestOutputName()

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
print(success_count, "songs successfully converted.")
if fail_count == 1:
    print(fail_count, "song failed to convert")
elif fail_count > 1:
    print(fail_count, "songs failed to convert.")
import random
import sys
import os
import eyed3

music_library = "E:\A\Music\Library"  # will eventually be specified by user
playlist_in = ""
playlist_name = ""
playlist_output_dir = "E:\A\Music\_python-playlists"  # will eventually be specified by user

def request_playlist():
    playlist = input("Please enter the absolute path of the playlist file:\n")
    extension = ""
    if len(playlist) > 4:
        extension = get_extension(playlist)
    while not os.path.isfile(playlist) or extension != ".m3u":
        if len(playlist) > 4:
            extension = get_extension(playlist)

        if playlist.upper() == "EXIT":
            print("Program exit")
            sys.exit(0)
        elif os.path.isdir(playlist):
            playlist = input("'" + playlist + "' is a directory not a file, please try again:\n")
        elif not os.path.isfile(playlist):
            playlist = input("File does not exist, please try again. Make sure you include the file extension!\n")
        elif not extension == ".m3u":
            playlist = input("File is not of type M3U [playlist.m3u], please try again:\n")
    print("Playlist file found! Importing " + playlist)
    return playlist;


def get_extension(input):

    # Reverse the filename to check whether it has a .m3u extension
    # If length is not more than 4 then it physically cannot have a .m3u extension
    rev = ""
    if len(input) > 4:
        rev = input[::-1]
        rev = rev[0:4]
        rev = rev[::-1]
    return rev.lower();


def request_output_name():
    name = input("Please enter a name for the converted playlist: ")
    while len(name) < 1:
        name = input("Invalid name. Please enter a valid name: ")

    # If the chosen filename does not include .m3u then add it
    if get_extension(name.lower()) != ".m3u":
        name += ".m3u"
    return name;


# Ask the user if the program should output absolute or relative paths in the playlist file
def absolute_or_relative():
    print("Should the playlist conversion output absolute or relative paths?")
    result = input("Please enter 'Absolute', 'Relative' or 'Exit': ").upper()
    while result not in ['ABSOLUTE', 'RELATIVE', 'EXIT']:
        result = input("Please enter 'Absolute', 'Relative' or 'Exit': ")
        result = result.upper()
        print("Result: " + result)
    if result == 'EXIT':
        print("Program exit")
        sys.exit(0)
    elif result == "ABSOLUTE":
        print("Absolute path selected for playlist output")
    elif result == "RELATIVE":
        print("Relative path selected for playlist output")
    return result;

print("------------------ Playlist Converter ------------------")

output_format = absolute_or_relative()
playlist_in = request_playlist()
playlist_name = request_output_name()
playlist_file = open(playlist_in, "r")

songs = []
success_count = 0;
fail_count = 0;

# Read playlist file and send results of each line to song list
for line in playlist_file:
    file_path = (os.path.dirname(playlist_in) + "\\" + line).rstrip()
    if os.path.isfile(file_path):
        audio_file = eyed3.load(file_path)
        artists = ""
        if audio_file.tag.artist is not None:
            artists = audio_file.tag.artist
        artists = artists.split(',')
        primary_artist = artists[0]
        album = ""
        if audio_file.tag.album is not None:
            album = audio_file.tag.album

        absolute_path = music_library + "\\" + primary_artist + "\\" + album + "\\" + line
        relative_path = primary_artist + "\\" + album + "\\" + line
        if not os.path.isfile(absolute_path.rstrip()):
            print("Warning: " + absolute_path.rstrip() + " does not exist in music library")
        else:
            if len(primary_artist) > 0 and len(album) > 0:
                if output_format == "ABSOLUTE":
                    songs.append(absolute_path)
                    success_count += 1
                elif output_format == "RELATIVE":
                    songs.append(relative_path)
                    success_count += 1
            else:
                print("Failed to convert: " + file_path)
                fail_count += 1
    else:
        print("Failed to convert: " + file_path)
        fail_count += 1
playlist_file.close()

# Playlist output location
playlist_output_path = ""
if output_format == "ABSOLUTE":
    playlist_output_path = playlist_output_dir + "\\" + playlist_name
elif output_format == "RELATIVE":
    playlist_output_path = music_library + "\\" + playlist_name

# Playlist output file operations
playlist_file_out = open(playlist_output_path, "w", encoding='utf-8')
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
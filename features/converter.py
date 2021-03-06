import sys
import os
import eyed3

"""
 | Playlist Converter
 | By Alex McGill
 | Latest Update: 24/08/2018
"""


# Get the path of the user music library directory
def get_music_library():
    library = input("Please enter the absolute path of the music library:\n")
    while not os.path.isdir(library):
        library = input("Please enter the absolute path of the music library:\n")
    print("Music library was successfully set to '" + library + "'")
    return library


# Get the input playlist path
def get_playlist():
    playlist = input("Please enter the absolute path of the playlist file:\n")
    extension = ""
    if len(playlist) > 4:
        extension = get_extension(playlist)
    while not os.path.isfile(playlist) or extension != ".m3u":
        if len(playlist) > 4:
            extension = get_extension(playlist)
        if playlist.upper() == "EXIT":
            print("Thanks for using Playlist Converter!")
            sys.exit(0)
        elif os.path.isdir(playlist):
            playlist = input("'" + playlist + "' is a directory not a file, please try again:\n")
        elif not os.path.isfile(playlist):
            playlist = input("File does not exist, please try again. Make sure you include the file extension!\n")
        elif not extension == ".m3u":
            playlist = input("File is not of type M3U [playlist.m3u], please try again:\n")
    print("Playlist file found! Importing " + playlist)
    return playlist


# Get the file extension from the playlist
def get_extension(file_name):
    # Reverse the filename to check whether it has a .m3u extension
    # If length is not more than 4 then it physically cannot have a .m3u extension
    rev = ""
    if len(file_name) > 4:
        rev = file_name[::-1]
        rev = rev[0:4]
        rev = rev[::-1]
    return rev.lower()


# Remove the extension from the file name
def remove_extension(file_name):
    if get_extension(file_name) == ".m3u":
        no_ext = file_name[:-4]
        return no_ext
    else:
        print("Error: Invalid file extension for output playlist")
        sys.exit(0)


# Get a name for the playlist output
def get_output_name():
    name = input("Please enter a name for the converted playlist:\n")
    while len(name) < 1:
        name = input("Invalid name. Please enter a valid name:\n")
    # If the chosen filename does not include .m3u then add it
    if get_extension(name.lower()) != ".m3u":
        name += ".m3u"
    return name


# Ask the user if the program should output absolute or relative paths in the playlist file
def absolute_or_relative():
    print("Should the playlist conversion output absolute or relative paths?")
    result = input("Please enter 'Absolute', 'Relative' or 'Exit':\n").upper()
    while result not in ['ABSOLUTE', 'RELATIVE', 'EXIT']:
        result = input("Please enter 'Absolute', 'Relative' or 'Exit':\n")
        result = result.upper()
        print("Result: " + result)
    if result == 'EXIT':
        print("Thanks for using Playlist Converter!")
        sys.exit(0)
    elif result == "ABSOLUTE":
        print("Absolute path selected for playlist output")
    elif result == "RELATIVE":
        print("Relative path selected for playlist output")
    return result


# Read playlist file and send results of each line to song list
def get_playlist_songs():
    attempts = 0
    for line in playlist_file:
        file_path = (os.path.dirname(playlist_in) + "\\" + line).rstrip()
        attempts += 1
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
                print("WARNING: " + absolute_path.rstrip() + " does not exist in music library")
            else:
                if len(primary_artist) > 0 and len(album) > 0:
                    if output_format == "ABSOLUTE":
                        songs.append(absolute_path)
                    elif output_format == "RELATIVE":
                        songs.append(relative_path)
                else:
                    print("Failed to convert: " + file_path)
        else:
            print("Failed to convert: " + file_path)
    playlist_file.close()
    return attempts


# Create the new playlist file and add the songs to it
def playlist_output():
    playlist_output_path = music_library + "\\" + playlist_name

    counter = 1
    while os.path.isfile(playlist_output_path):
        counter += 1
        playlist_output_path = music_library + "\\" + remove_extension(playlist_name) + " (" + str(counter) + ").m3u"

    # Playlist output file operations
    playlist_file_out = open(playlist_output_path, "w", encoding='utf-8')
    playlist_file_out.write("# Converted with Playlist Converter by Alex McGill\n")
    playlist_file_out.write("# " + playlist_name + "\n")
    playlist_file_out.writelines(songs)
    playlist_file_out.close()


# Display conversion results
def display_results():
    success_count = len(songs)
    fail_count = attempt_count - success_count

    if fail_count == 0:
        print("All songs successfully converted!")
    elif success_count == 0:
        print("No songs were successfully converted")
    elif success_count == 1:
        print(success_count, "/", (success_count+fail_count), "song successfully converted")
    else:
        print(success_count, "/", (success_count+fail_count), "songs successfully converted")


# Declaring variables
output_format = ""
playlist_in = ""
playlist_name = ""
playlist_file = ""

songs = []
attempt_count = ""
run_count = 0

# Main program
while True:
    print("\n------------------ Playlist Converter ------------------")

    if run_count == 0:
        music_library = get_music_library()

    output_format = absolute_or_relative()
    playlist_in = get_playlist()
    playlist_name = get_output_name()
    playlist_file = open(playlist_in, "r")

    songs = []
    attempt_count = get_playlist_songs()

    playlist_output()
    display_results()

    print("--------------------------------------------------------")

    repeat = input("\nWould you like to convert another playlist? (YES/NO):\n")
    while repeat.upper().strip() not in ["YES", "NO"]:
        repeat = input("Would you like to convert another playlist? (YES/NO):\n")
    if repeat.upper().strip() == "NO":
        print("Thanks for using Playlist Converter!")
        sys.exit(0)
    else:
        run_count += 1
        continue

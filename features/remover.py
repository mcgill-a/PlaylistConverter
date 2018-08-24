import sys
import os

"""
 | Playlist Remover
 | By Alex McGill
 | Latest Update: 24/08/2018
"""

# Declare variables
directory = ""
confirm = ""


# Get directory path
def get_directory():
    input_dir = input("Please enter the absolute path of the directory:\n")
    while not os.path.isdir(input_dir):
        if input_dir.upper() == "EXIT":
            print("Thanks for using Playlist Remover!")
            sys.exit(0)
        elif os.path.isfile(input_dir):
            input_dir = input("'" + input_dir + "' is a file not a directory, please try again:\n")
        elif not os.path.isdir(input_dir):
            input_dir = input("Directory does not exist, please try again\n")
    return input_dir


# Remove any files named playlist.m3u from sub-dirs
def remove_files(path):
    count = 0
    for subdir, dirs, files in os.walk(path):
        for file in files:
            if file == "playlist.m3u":
                full_name = os.path.join(subdir, file)
                os.remove(full_name)
                count += 1
    if count != 1:
        print("Removed", count, "files")
    else:
        print("Removed", count, "file")


directory = get_directory()

while confirm not in ["YES", "NO"]:
    confirm = input("Do you want to remove all 'playlist.m3u' files from this directory? (YES/NO/EXIT):\n").upper()
    if confirm == "NO":
        directory = get_directory()
    elif confirm == "YES":
        remove_files(directory)
    elif confirm == "EXIT":
        print("Thanks for using Playlist Remover!")
        sys.exit(0)

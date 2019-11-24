#! /bin/env python3

import glob
import os
from pathlib import Path

#arguments
dir = 'home/'
verify = True
ignore_files = ['onedrive']

def ignore(path: str):
    for ignore in ignore_files:
        if path.find(ignore) != -1:
            return True
    return False


repo_directory = os.path.dirname(os.path.abspath(__file__))
print("Configuration repo in "+ repo_directory)
files_to_link = []

for filename in glob.iglob(dir + '**', recursive=True):
    if Path(filename).is_file():
        files_to_link.append(filename[len(dir):])

print("Found {} files to link".format(len(files_to_link)))

print("Switching directory to ~")

os.chdir(os.path.expanduser('~'))

for file in files_to_link:
    target_link = "." + file
    repo_file = repo_directory + "/" + dir + file
    if verify:
        file = Path(target_link)
        if not file.is_symlink() and file.exists():
            print("Target link {} exists, this file will be removed if linked".format(target_link))
        if not file.exists():
            print("Target link {} can be linked".format(target_link))
        if file.is_symlink():
            print("{} is a symlink".format(target_link))
    elif not ignore(target_link):
        #check if the symlink directory exists, if not, create it:
        target_directory = target_link[:target_link.rfind("/")]
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        #if the file exists, delete it
        if os.path.exists(target_link):
            os.remove(target_link)
        print("Linking {} -> {}".format(target_link, repo_file))
        os.symlink(repo_file, target_link)
    else:
        print("Ignoring " + target_link)

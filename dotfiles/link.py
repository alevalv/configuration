#! /bin/env python3
# This script will verify or link all files in the `home` folder that accompanies this script
# they will be linked to your home directory, replacing any existing file.

import argparse
import glob
import os
from pathlib import Path

# arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "-l",
    "--link",
    type=bool,
    help="Sets the script to link all files (will replace existing files)",
    nargs='?',
    default=False,
    const=True)
parser.add_argument(
    '-i',
    '--ignore',
    type=str,
    help="A list of files that should be ignored when linking",
    nargs='*',
    default=['onedrive'])
home_directory = 'home/'
args = parser.parse_args()
print("files/directories {} will be ignored".format(args.ignore))


def ignore(path: str):
    for ignore_file in args.ignore:
        if path.find(ignore_file) != -1:
            return True
    return False


repo_directory = os.path.dirname(os.path.abspath(__file__))
print("Configuration repo in " + repo_directory)
files_to_link = []

for filename in glob.iglob(home_directory + '**', recursive=True):
    if Path(filename).is_file():
        files_to_link.append(filename[len(home_directory):])

print("Found {} files to link".format(len(files_to_link)))

print("Switching directory to ~")

os.chdir(os.path.expanduser('~'))

for file in files_to_link:
    target_link = "." + file
    repo_file = repo_directory + "/" + home_directory + file
    if not args.link:
        file = Path(target_link)
        if not file.is_symlink() and file.exists():
            print("Target link {} exists, this file will be removed if linked".format(target_link))
        if not file.exists():
            print("Target link {} can be linked".format(target_link))
        if file.is_symlink():
            print("{} is a symlink".format(target_link))
    elif not ignore(target_link):
        # check if the linking target is inside a directory
        if "/" in target_link:
            # check if the symlink directory exists, if not, create it:
            target_directory = target_link[:target_link.rfind("/")]
            if not os.path.exists(target_directory):
                os.makedirs(target_directory)
        # if the file exists, delete it
        if os.path.exists(target_link):
            os.remove(target_link)
        print("Linking {} -> {}".format(target_link, repo_file))
        os.symlink(repo_file, target_link)
    else:
        print("Ignoring " + target_link)

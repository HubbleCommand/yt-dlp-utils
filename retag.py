from mutagen.easyid3 import EasyID3
import argparse
import os
import pathlib

"""
A now fairly pontless utility, delete later
"""
#https://docs.python.org/3/howto/argparse.html
parser = argparse.ArgumentParser()

parser.add_argument("-d", "--directory", help="path to directory to retag", type=str)
args = parser.parse_args()
parser.parse_args()
print(EasyID3.valid_keys.keys())
dir = os.getcwd()
if args.directory:
    dir = args.directory


for i, mp3 in enumerate([f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f.endswith(".mp3")]):
    tags = EasyID3(os.path.join(dir, mp3))

    #https://mutagen.readthedocs.io/en/latest/user/id3.html
    split = mp3.split(" - ")
    if len(split) == 2:
        tags['artist'] = split[0]
        tags['title'] = pathlib.Path(split[1]).stem
    else:
        tags['title'] = pathlib.Path(mp3).stem
    tags['album'] = os.path.basename(os.path.normpath(dir))
    tags['tracknumber'] = f"{i}"

    tags.save()
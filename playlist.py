from mutagen.easyid3 import EasyID3 #I don't think this will be needed for playlists... only to write track number maybe
import argparse
import os
import subprocess
import datetime
from common_argparse import make_common_argparse, parse_common_args_url

"""
Python utility script to download a YT playlist and diff from an already downloaded version of it
https://gist.github.com/HubbleCommand/3d64767a952dc0ac709d2ee43b814cb3
https://gist.github.com/HubbleCommand/fa607cb86b023b08e04164ee650407fb
"""

def main():
    stamp_start = datetime.datetime.now().timestamp()
    #https://docs.python.org/3/howto/argparse.html
    parser = make_common_argparse()
    parser.add_argument("--start", help="index to start at", type=int)
    parser.add_argument("-o", "--operation", help="merge operation to use if dir isn't empty; r to merge by renaming, d to merge by deleting", type=str)
    args = parser.parse_args()
    parser.parse_args()

    url, id, dir, video, subtitle, err = parse_common_args_url(args = args, url_start="https://www.youtube.com/playlist?list")

    if err:
        return

    #This may take an exceeding amount of time, depending on the length of the playlist...
    #command = f'yt-dlp.exe --rm-cache-dir -ciw --embed-thumbnail --embed-metadata --extract-audio --audio-format mp3 -o "{dir}/%(playlist_index)s - %(title)s.%(ext)s" {url}'
    command = 'yt-dlp.exe --rm-cache-dir -ciw --embed-thumbnail --embed-metadata '
    if args.start:
        command += f' --playlist-start {args.start} '
    if not video:
        command += '--extract-audio --audio-format mp3 '
    command += f'-o "{dir}/%(playlist_index)s - %(title)s.%(ext)s" {url}'
    download = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) #run(..., capture_output=True, text=True)
  
    #For logging yt-dlp progress, pipe the output here
    while download.stdout.readable():
        line = download.stdout.readline()

        if not line:
            break

        #To avoid log pollution, don't print the download percentages (only prints a bulk message anyways)
        if "[download]" in str(line) and "0.0%" in str(line):
            continue

        print(line.strip())
    
    if download.stderr:
        print(f"{download.returncode} - {download.stderr}")
        return
    
    stamp_dl_end = datetime.datetime.now().timestamp()
    print(f"elapsed time downloading: {stamp_dl_end - stamp_start}")
    #If no merge operation specified, just quit
    if not args.operation:
        return
    
    mp3s = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f.endswith(".mp3")]
    for mp3 in reversed(mp3s):
        fname = os.path.basename(mp3)
        tnumber, name = fname.rsplit('.', 1)[0].split(" - ", 1) #reverse split to remove extension, then forward split to split track number & actual name

        #if any(name in t for t in mp3s):
        if len([t for t in mp3s if name in t]) > 1:
            print("Found duplicate, deleting")
            os.remove(os.path.join(dir, mp3))
            #TODO I'm pretty sure we want to keep the one with the lowest track id, so that would mean we should jsut reverse the list?

if __name__ == "__main__":
    main()

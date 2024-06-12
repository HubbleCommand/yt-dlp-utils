import argparse
import os
import datetime
import shutil
from pathlib import Path

"""
Python utility script that handles the merging of downloaded playlists, specifically to merge back deleted videos

Example call: python merge.py -p ./dir1 ./dir2 -o ./out
"""

def main():
    stamp_start = datetime.datetime.now().timestamp()
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--playlists", help="paths (absolute or relative) of the playlists to merge", type=str, nargs="+", default="/path")
    parser.add_argument("-o", "--out", help="output directory, files will be dumped here", type=str, default="/path")
    args = parser.parse_args()
    parser.parse_args()

    out = Path(args.out)
    if not out.exists():
        out.mkdir(parents=True)

    songs = []

    for playlist in args.playlists:
        p = Path(playlist)
        
        for child in p.iterdir():
            song_name = child.name.split(" - ", 1)[1]  # Remove playlist index
            song_name = song_name.rsplit(".", 1)[0]   # Remove file type
            
            if song_name not in songs:
                songs.append(song_name)
                shutil.copy2(child.absolute(), out.absolute())
    
    print(f"Unique songs {len(songs)}")

    stamp_cpy_end = datetime.datetime.now().timestamp()
    print(f"elapsed copy time : {stamp_cpy_end - stamp_start}")

    ## Lastly, verify that the out dir has no duplicate song names
    print("Copy done, verifying")
    num_files = len([f for f in os.listdir(out.absolute()) if os.path.isfile(os.path.join(out.absolute(), f))])
    if num_files != len(songs):
        print(f"Mismatch, expected {len(songs)} but found {num_files}")
    
    out_songs = []
    for child in out.iterdir():
        if child in out_songs:
            print(f"Duplicate file found for {child}")
            continue
        out_songs.append(child)

    stamp_end = datetime.datetime.now().timestamp()
    print(f"verification elapsed time : {stamp_end - stamp_cpy_end}")
    print(f"Total elapsed time : {stamp_end - stamp_start}")

if __name__ == "__main__":
    main()

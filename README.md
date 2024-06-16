# YT-DLP Utils
Wrapper commands around common [YT-DLP](https://github.com/yt-dlp/yt-dlp) commands that I use

> YT-DLP can be used to download videos from a much wider source than I imagined, including LinkedIn! See [this page](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) for the full list.

## Setup
Download the yt-dlp executable from the [yt-dlp repo](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#installation).

You will need ffmpeg for the metadata and file splitting features. yt-dlp provides custom builds of this critical dependency [here](https://github.com/yt-dlp/FFmpeg-Builds?tab=readme-ov-file).

You can either use these scripts within the same directory as the installed requirements, or add `yt-dlp.exe`, `ffmpeg`, `ffplay`, and `ffprobe` to your system's `PATH` variables.

Install the python dependencies with `pip install -r requirements.txt`

## Leftover commands
These are some commands that are too short to write a complete script for

- Download only video thumbnail : `yt-dlp --write-thumbnail --skip-download <URL>`


## Single
Downloads a single video as a `.mp3` file.

```
python chapters.py
    --dir       str: 'absolute path to write results to'
    --url       str: 'video url'
    --video     flag: 'download full videos instead of converting to mp3s'
```

## Chapters
Downloads a single video, seperating it into separate files by chapter.

```
python chapters.py
    --dir       str: 'absolute path to write results to'
    --id        str: 'video id (youtube only)'
    --url       str: 'video url'
```

## Playlist
Downloads a playlist, can handle merging with previous downloads if set.

```
python playlist.py
    --dir       str: 'absolute path to write results to'
    --id        str: 'playlist id (youtube only)'
    --url       str: 'playlist url'
    --video     flag: 'download full videos instead of converting to mp3s'
    --start     int: 'start download from playlist index'
    --operation str: 'merge operation used if dir isn't empty; r to merge by 
                        renaming, d to merge by deleting'
```

## Merge
Merges downloaded playlists directories, specifically to merge back deleted videos. Does so by copying all unique files in supplied folders to the output directory (ignoring index & file type).

```
python merge.py
    --playlists  str+: 'paths to the playlist directories'
    --out         str: 'where to copy files to'
```

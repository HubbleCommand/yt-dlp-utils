# YT-DLP Utils
Wrapper commands around common [YT-DLP](https://github.com/yt-dlp/yt-dlp) commands that I use

> YT-DLP can be used to download videos from a much wider source than I imagined, including LinkedIn!

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
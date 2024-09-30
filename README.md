# YT-DLP Utils
Wrapper commands around common [YT-DLP](https://github.com/yt-dlp/yt-dlp) commands that I use

> YT-DLP can be used to download videos from a much wider source than I imagined, including LinkedIn! See [this page](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) for the full list.

## Setup
Download the yt-dlp executable from the [yt-dlp repo](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#installation).

You will need ffmpeg for the metadata and file splitting features. yt-dlp provides custom builds of this critical dependency [here](https://github.com/yt-dlp/FFmpeg-Builds?tab=readme-ov-file).

You can either use these scripts within the same directory as the installed requirements, or add `yt-dlp.exe`, `ffmpeg`, `ffplay`, and `ffprobe` to your system's `PATH` variables.

Install the python dependencies with `pip install -r requirements.txt`

Note that there are possible limitations with metadata tags.
[Mutagen EasyID3](https://mutagen.readthedocs.io/en/latest/api/id3.html#module-mutagen.easyid3) is used, which has the following available tags:

```
print(EasyID3.valid_keys.keys())
dict_keys([
    'album', 'bpm', 'compilation', 'composer', 'copyright', 'encodedby', 'lyricist', 'length', 'media', 'mood', 'grouping', 'title',
    'version', 'artist', 'albumartist', 'conductor', 'arranger', 'discnumber', 'organization', 'tracknumber', 'author',
    'albumartistsort', 'albumsort', 'composersort', 'artistsort', 'titlesort', 'isrc', 'discsubtitle', 'language',
    'genre', 'date', 'originaldate', 'performer:*', 'musicbrainz_trackid', 'website', 'replaygain_*_gain', 'replaygain_*_peak',
    'musicbrainz_artistid', 'musicbrainz_albumid', 'musicbrainz_albumartistid', 'musicbrainz_trmid', 'musicip_puid', 'musicip_fingerprint',
    'musicbrainz_albumstatus', 'musicbrainz_albumtype', 'releasecountry', 'musicbrainz_discid', 'asin', 'performer', 'barcode', 'catalognumber',
    'musicbrainz_releasetrackid', 'musicbrainz_releasegroupid', 'musicbrainz_workid', 'acoustid_fingerprint', 'acoustid_id'
])
```

## Leftover commands
These are some commands that are too short to write a complete script for

- Download only video thumbnail : `yt-dlp --write-thumbnail --skip-download <URL>`


## Single
Downloads a single video as a `.mp3` file.

```
python single.py
    --dir       str: 'absolute path to write results to'
    --id        str: 'playlist id (youtube only)'
    --url       str: 'playlist url'
    --video     flag: 'download full videos instead of converting to mp3s'
```

## Chapters
Downloads a single video, seperating it into separate files by chapter.

** WARNING ** thumbnail might not be embedded, see [this issue](https://github.com/yt-dlp/yt-dlp/issues/6225) for details

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

from mutagen.easyid3 import EasyID3
import argparse
import os
import subprocess
from glob import glob

"""
Python utility script that wraps yt-dlp to download a single video and split it into chapters, while correctly setting the metadata of each file (which yt-dlp currently cannot do)

Example call: python chapters.py -u https://www.youtube.com/watch?v=FeaZxmtDNWk
"""
def main():
    #https://docs.python.org/3/howto/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="output directory", type=str)
    parser.add_argument("-u", "--url", help="video url", type=str) #, nargs='+'
    parser.add_argument("--id", help="video id", type=str) #, nargs='+'
    parser.add_argument("-o", "--override-name", help="override the target folder name", type=str)
    args = parser.parse_args()
    parser.parse_args()

    """
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
    """

    """
    if not args.url:
        print("URL required")
        return
    url = args.url
    id = url.rsplit("=", 2)[1]
    """
    url = None
    id = None
    if not args.url:
        if not args.id:
            print("URL or video ID required")
            return
        url = f"https://www.youtube.com/watch?v={args.id}"
        id = args.id
    else:
        url = args.url
        split = url.rsplit("=", 1)
        if len(split) >= 2:
            id = split[1]
        else:
            id = ""

    print(f"Video ID: {id}")

    dir = os.getcwd()
    if args.directory:
        dir = args.directory #os.path.abspath(args.directory)

    download = subprocess.Popen(f'yt-dlp --rm-cache-dir --extract-audio --audio-format mp3 --embed-thumbnail --embed-metadata --split-chapters -o "chapter:{dir}/%(title)s - {id}/%(section_number)s - %(section_title)s.%(ext)s" {url}', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    #For logging yt-dlp progress, pipe the output here
    while download.stdout.readable():
        line = download.stdout.readline()

        if not line:
            break

        stringified = str(line)
        #To avoid log pollution, don't print the download percentages (only prints a bulk message anyways)
        if "[download]" in stringified and "0.0%" in stringified:
            continue

        if "[ExtractAudio]" in stringified:
            #Here, can get the file name that isn't always cleaned up by yt-dlp
            tmp = stringified.split("Destination: ", 1)[1]
            #TODO delete this tmp file if yt-dlp doesn't

        print(line.strip())

    if download.stderr:
        print(f"{download.returncode} - {download.stderr}")
        #TODO clear directory
        return

    print("     Finished download, retagging")
    """
    output = subprocess.run(f'yt-dlp --rm-cache-dir --dump-json --skip-download --split-chapters {url}', capture_output=True, text=True)
    chapters = json.loads(output.stdout)["chapters"]
    """

    #Get the folder bath based on ID
    dfolder = glob(f"*{id}", root_dir=dir)  #destination folder, where yt-dlp downloaded and split the files
    if len(dfolder) != 1:
        print("Error while finding folders")
        return

    album = dfolder[0].rsplit(" - ", 1)[0]
    print(f"album: {album}")

    dfolder_path = os.path.join(dir, dfolder[0]) #os.path.join(dir, id)
    mp3s = [f for f in os.listdir(dfolder_path) if os.path.isfile(os.path.join(dfolder_path, f)) and f.endswith(".mp3")]
    for mp3 in mp3s:
        tags = EasyID3(os.path.join(dfolder_path, mp3))

        #First, split the file name to extract the chapter index
        fname = os.path.basename(mp3)
        tnumber, name = fname.rsplit('.', 1)[0].split(" - ", 1) #reverse split to remove extension, then forward split to split track number & actual name

        #https://mutagen.readthedocs.io/en/latest/user/id3.html
        split = name.split(" - ")
        if len(split) == 2:
            tags['artist'] = split[0]
            tags['title'] = split[1]
        else:
            tags['title'] = name
        tags['album'] = album #os.path.basename(os.path.normpath(dir))
        tags['tracknumber'] = f"{tnumber}"
        tags.save()

    #Finally, write a metadata file to save url & other useful data
    """
    metadata = {
        'url': url
    }

    with open(os.path.join(dfolder_path, "metadata.json"), 'w', encoding='utf-8') as f:
        json.dump(metadata, f)
    """

if __name__ == "__main__":
    main()

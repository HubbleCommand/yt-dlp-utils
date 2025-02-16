import argparse
import os
import subprocess
from common_argparse import make_common_argparse, parse_common_args_url

def main():
    parser = make_common_argparse()
    parser.add_argument("-v", "--video", help="download as video instead of converting to mp3", action="store_true")
    parser.add_argument("-t", "--trim", help='trim "*from-to" ie "*25-32", all in seconds')
    args = parser.parse_args()
    parser.parse_args()

    url, id, dir, err = parse_common_args_url(args = args, url_start="https://www.youtube.com/watch?v")

    if err:
        return

    command = 'yt-dlp.exe --rm-cache-dir -ciw --embed-thumbnail --embed-metadata '
    if not args.video:
        command += '--extract-audio --audio-format mp3 '
    if args.trim:
        command += f" --download-sections {args.trim} "
    
    command += f'-o "{dir}/%(title)s - {id}.%(ext)s" {url}'
    download = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  
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

if __name__ == "__main__":
    main()
    
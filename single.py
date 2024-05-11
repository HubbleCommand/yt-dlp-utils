import argparse
import os
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="output directory, MUST be a full path, files will be dumped here, this script handles merging", type=str)
    parser.add_argument("-u", "--url", help="playlist video url", type=str) #, nargs='+'
    args = parser.parse_args()
    parser.parse_args()

    if not args.url:
        print("URL required")
        return
    url = args.url
    dir = os.getcwd()
    if args.directory:
        dir = args.directory #os.path.abspath(args.directory)

    download = subprocess.Popen(f'yt-dlp --rm-cache-dir --extract-audio --audio-format mp3 --embed-thumbnail --embed-metadata -o "/{dir}/%(title)s.%(ext)s" {url}', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  
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
    
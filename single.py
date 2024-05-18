import argparse
import os
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="output directory, MUST be a full path, files will be dumped here", type=str)
    parser.add_argument("-u", "--url", help="video url", type=str) #, nargs='+'
    parser.add_argument("-v", "--video", help="download as video instead of converting to mp3", action="store_true")
    args = parser.parse_args()
    parser.parse_args()

    if not args.url:
        print("URL required")
        return
    url = args.url
    dir = os.getcwd()
    if args.directory:
        dir = args.directory #os.path.abspath(args.directory)

    command = 'yt-dlp.exe --rm-cache-dir -ciw --embed-thumbnail --embed-metadata '
    if not args.video:
        command += '--extract-audio --audio-format mp3 '
    command += f'-o "{dir}/%(title)s.%(ext)s" {url}'
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
    
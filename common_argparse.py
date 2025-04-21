import argparse
import os

def make_common_argparse():
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--directory", help="output directory, MUST be a full path, files will be dumped here, this script handles merging", type=str)
	parser.add_argument("-v", "--video", help="if download as a video instead of just audio", action="store_true")
	parser.add_argument("-u", "--url", help="video / playlist url", type=str) #, nargs='+'
	parser.add_argument("--id", help="video / playlist id", type=str) #, nargs='+'
	return parser

def parse_common_args_url(args, url_start):
	url = None
	id = None
	if not args.url :
		if not args.id:
			print("URL or video ID required")
			return [None, None, None, True]
		url = f"{url_start}={args.id}"
		id = args.id
	else:
		url = args.url
		try:
			id = url.rsplit("=", 1)[1]
		except:
			id = None

	dir = os.getcwd()
	if args.directory:
		dir = args.directory #os.path.abspath(args.directory)
	
	vid = args.video

	return [url, id, dir, vid, None]
    

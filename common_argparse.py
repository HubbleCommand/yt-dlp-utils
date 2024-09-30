import argparse
import os

def make_common_argparse():
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--directory", help="output directory, MUST be a full path, files will be dumped here, this script handles merging", type=str)
	parser.add_argument("-u", "--url", help="playlist url", type=str) #, nargs='+'
	parser.add_argument("--id", help="playlist id", type=str) #, nargs='+'
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
		id = url.rsplit("=", 1)[1]

	dir = os.getcwd()
	if args.directory:
		dir = args.directory #os.path.abspath(args.directory)

	return [url, id, dir, None]
    

#! /usr/bin/env python3

# This program will read in a file containing line separated URLs from yande.re,
# extract the high resolution image URL, and download the image into the CWD.

import requests
from urllib.parse import unquote
import time

from requests.models import HTTPError
#import argparse


#parser = argparse.ArgumentParser(prog="yande.re-downloader", description="Download images from yande.re")
#parser.add_argument("input file", type=path, help="a file from which URLs can be taken")
#parser.add_argument(["-w","--wait"], type=int, default=3, help="number of seconds to wait between #operations")
#args = parser.parse_args()



def get_urls_from_file(input_file):
	with open("download") as f:
		return [line.strip() for line in f.readlines() if line[0] == 'h']


def get_page_html(page_url):
	print(page_url)
	r = requests.get(page_url)
	html_page = r.text
	return html_page


def get_image_url(html_page):
	# The full res image link is either tagged 'id="highres"' or 'id="png"'; PNG is preferred.
	raw_image_url = ""
	for line in html_page.splitlines():
		if 'id="png"' in line:
			raw_image_url = line
		elif 'id="highres"' in line:
			raw_image_url = line
	image_url = raw_image_url.split(" ")
	for part in image_url:
		if 'href=' in part:
			image_url = part.split('"')
	for part in image_url:
		if 'http' in part:
			image_url = part
	print(image_url)
	return image_url


def download_image(image_url):
	try:
		r = requests.get(image_url)
		r.raise_for_status()
		filename = unquote(image_url.split('/')[-1])
		with open(filename,'wb') as output_file:
			output_file.write(r.content)
	except HTTPError:
		print("HTTP error: Status code {0} from {1}".format(r.status_code, r.url))
	print("Downloaded!")
	time.sleep(3)


def page_url_to_image(page_url):
	download_image(get_image_url(get_page_html(page_url)))


for url in get_urls_from_file("file"):
	page_url_to_image(url.strip())

print("███████████████\n███  DONE!  ███\n███████████████")

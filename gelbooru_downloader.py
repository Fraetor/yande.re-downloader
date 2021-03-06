#! /usr/bin/env python3

# This program will read in a file containing line separated URLs from yande.re,
# extract the high resolution image URL, and download the image into the CWD.

import requests
from urllib.parse import unquote
import time
#import argparse


#parser = argparse.ArgumentParser(prog="yande.re-downloader", description="Download images from yande.re")
#parser.add_argument("input file", type=path, help="a file from which URLs can be taken")
#parser.add_argument(["-w","--wait"], type=int, default=3, help="number of seconds to wait between #operations")
#args = parser.parse_args()



def get_urls_from_file(input_file):
	with open("download") as f:
		return f.readlines()


def get_page_html(page_url):
	print(page_url)
	r = requests.get(page_url)
	html_page = r.text
	return html_page


def get_image_url(html_page):
	# The full res image link has the text "Original image".
	raw_image_url = ""
	for line in html_page.splitlines():
		for subline in line.split("<li>"):
			if 'Original image' in subline:
				raw_image_url = subline
				#print(raw_image_url)
				#input("ENTER to continue.")
	image_url = raw_image_url.split(" ")
	for part in image_url:
		if 'href=' in part:
			image_url = part.split('"')
	for part in image_url:
		if 'http' in part:
			image_url = part
	print(image_url)
	#input("ENTER to continue.")
	return image_url


def download_image(image_url):
	r = requests.get(image_url)
	if r.status_code == 200:
		print("Downloaded: {}".format(r.status_code))
		filename = unquote(image_url.split('/')[-1])
		with open(filename,'wb') as output_file:
			output_file.write(r.content)
	else:
		print("Download Failed: {}".format(r.status_code))
	time.sleep(3)


def page_url_to_image(page_url):
	download_image(get_image_url(get_page_html(page_url)))


for url in get_urls_from_file("file"):
	page_url_to_image(url.strip())

print("███████████████\n███  DONE!  ███\n███████████████")

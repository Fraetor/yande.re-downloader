#! /usr/bin/env python3

# This program will read in a file containing line separated URLs from yande.re,
# extract the high resolution image URL, and download the image into the CWD.

import requests
from urllib.parse import unquote


def get_urls_from_file(input_file):
	with open("download") as f:
		return f.readlines()


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
	r = requests.get(image_url)
	filename = unquote(image_url.split('/')[-1])
	with open(filename,'wb') as output_file:
		output_file.write(r.content)
	print("Downloaded!")


def page_url_to_image(page_url):
	download_image(get_image_url(get_page_html(page_url)))


for url in get_urls_from_file("file"):
	page_url_to_image(url.strip())

print("███████████████\n███  DONE!  ███\n███████████████")

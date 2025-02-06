#! /usr/bin/env python3

# This program will read in a file containing line separated URLs from yande.re,
# extract the high resolution image URL, and download the image into the CWD.

import requests
from urllib.parse import unquote
import time
import random


def get_urls_from_file(input_file):
    with open("download") as f:
        return list(
            filter(
                lambda l: l.startswith("https://gelbooru.com/"),
                (l.strip() for l in f.readlines()),
            )
        )


def get_page_html(page_url):
    r = requests.get(page_url)
    html_page = r.text
    return html_page


def get_image_url(html_page):
    # The full res image link has the text "Original image".
    raw_image_url = ""
    for line in html_page.splitlines():
        for subline in line.split("<li>"):
            if "Original image" in subline:
                raw_image_url = subline
    image_url = raw_image_url.split(" ")
    for part in image_url:
        if "href=" in part:
            image_url = part.split('"')
    for part in image_url:
        if "http" in part:
            image_url = part
    return image_url


def download_image(image_url):
    r = requests.get(image_url)
    if r.status_code == 200:
        print(f"Downloaded: {r.status_code}")
        filename = unquote(image_url.split("/")[-1])
        with open(filename, "wb") as output_file:
            output_file.write(r.content)
    else:
        print(f"Download Failed: {r.status_code}")
    # Randomly wait between 2 and 5 seconds.
    time.sleep(2 + 3 * random.random())


def page_url_to_image(page_url):
    print(f"Fetching HTML for {page_url}")
    page_html = get_page_html(page_url)
    image_url = get_image_url(page_html)
    print(f"Fetching image from {image_url}")
    download_image(image_url)


for url in get_urls_from_file("file"):
    page_url_to_image(url)

print("███████████████\n███  DONE!  ███\n███████████████")

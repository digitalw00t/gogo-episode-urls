#!/usr/bin/env python3

import re
import sys
import json
import requests
from bs4 import BeautifulSoup

dict = {}
dict = {'episodes': []}

filename = 'infodump.json'

# Get the URL from command line argument
if len(sys.argv) != 2:
    print("Usage: python webscraper.py <url>")
    sys.exit(1)


dict['gogoanime'] = sys.argv[1]
url = "https://gogoanime3.net/" + sys.argv[1]
dict['url'] = url

# Send a GET request to the webpage you want to scrape
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")


print(soup)
#sys.exit(0)
download_div = soup.find("div", {"class": "cf-download"})
if download_div is not None:
    # Find all the <a> elements inside the <div class="cf-download"> element
    download_links = download_div.find_all("a")
    # Loop through the links and print the URL and title
    for link in download_links:
        link_url = link["href"]
        link_title = link.text.strip()
        print(link_url, link_title)
else:
    print("No download links found.")

#for key, value in dict.items():
#    print(key,": ", value)


print("------------------------------------------------")
print(f"Title: {dict['title']}")
print(f"\tStatus: {dict['status']}")

with open(filename, "w") as outfile:
    json.dump(dict, outfile, indent=4)



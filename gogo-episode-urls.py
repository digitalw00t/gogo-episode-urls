#!/usr/bin/env python3
# Program: gogoanime-show_info.py
# Author: Draeician (2023-08017)

# Base URL - change this variable if the domain changes
BASE_URL = "https://gogoanime3.net/"

# Importing required libraries
import requests
import re
from bs4 import BeautifulSoup
import argparse
import json

__VERSION__ = "v0.1.0"

# Global debug level variable
DEBUG_LEVEL = 0

def parse_arguments():
    """Parse command-line arguments."""
    global DEBUG_LEVEL
    parser = argparse.ArgumentParser(description='gogoanime-show_info.py: Web scraping script for gogoanime3.net')
    parser.add_argument('url_part', help='The part of the URL to be scraped (e.g., "isekai-nonbiri-nouka-dub")')
    parser.add_argument('--debug', type=int, choices=[0, 1, 2, 3], default=0, help='Set debug level (0: None, 1: Info, 2: Verbose, 3: Full HTML dump)')
    args = parser.parse_args()
    DEBUG_LEVEL = args.debug
    return args

def send_request(url):
    """Send a GET request to the specified URL and return the BeautifulSoup object."""
    response = requests.get(url)
    display(f"Request sent to {url}. Status code: {response.status_code}", verbosity=2)
    return BeautifulSoup(response.content, "html.parser")

def extract_anime_info(soup):
    """Extract anime information from the HTML content."""
    main_body_div = soup.find("div", {"class": "main_body"})
    anime_details = {} # To store the details

    # Extracting the title
    anime_title = main_body_div.find("h1").text if main_body_div else "Title not found"
    anime_details['title'] = anime_title
    display(f"Anime Title: {anime_title}", verbosity=1)

    # Extracting the number of episodes which would be the last episode
    all_episodes = soup.find("ul", {"id": "episode_page"})
    if all_episodes:
        last_episode = int(list(filter(None, "-".join(all_episodes.get_text().splitlines()).split("-")))[-1].strip())
        anime_details['number_of_episodes'] = last_episode
    else:
        raise Exception("Last Episode not found")
    display(f"Last Episode: {last_episode}", verbosity=1)

    # Using the provided query
    div_element = soup.find('div', class_='bg-notice', style='position:fixed;z-index:9999;background:#ffc119;bottom:0;text-align:center;color:#000;width:100%;padding:10px 0;font-weight:600;')

    # Extracting the content inside the div
    pattern = r'We moved site to (.*?)\. Please bookmark new site\. Thank you!'
    match = re.search(pattern, div_element.text)
    anime_details['new_site'] = match.group(1).lower() if match else None
    display(f"New Site: {anime_details['new_site']}", verbosity=1)

    # Extracting Genre
    genre_div = soup.find('div', class_='anime_info_body_bg')
    genre = genre_div.text if genre_div and soup.find("p", {"class": "type"}) else "Genre not found"
    genre = genre.replace(": \n", ":")


    anime_details['genre'] = genre
    display(f"Genre: {genre}", verbosity=1)

    # Extracting the status, type, released, and other name
    categories = ["Genre", "Status", "Type", "Released", "Other name", "Plot Summary"]
    values = [re.search(fr"{category}:\s*(.*?)(?:\n|$)", genre).group(1) for category in categories]
    anime_details['genre'] = values[0]
    anime_details['status'] = values[1]
    anime_details['type'] = values[2]
    anime_details['released'] = values[3]
    anime_details['other_name'] = values[4]
    anime_details['plot_summary'] = values[5]

    display(f"Values: {values}", verbosity=1)    

    return anime_details

def display(message, verbosity=1):
    """Display a message based on verbosity level."""
    if verbosity <= DEBUG_LEVEL:
        print(message)

def main():
    # Parsing command-line arguments
    args = parse_arguments()

    # Constructing the full URL using the BASE_URL
    url_part = args.url_part
    url = BASE_URL + f"category/{url_part}"
    display(f"URL: {url}\n", verbosity=1)

    # Sending the request and getting the BeautifulSoup object
    soup = send_request(url)

    # Dumping the entire HTML content if debug level is 3
    display(f"Full HTML Content: {soup.prettify()}", verbosity=3)

    # Extracting anime information
    anime_details = extract_anime_info(soup)

    # Writing the data to a JSON file
    filename = 'infodump.json'
    data_dict = {
        'gogoanime': url_part,
        'url': url,
        'anime_details': anime_details
    }
    with open(filename, "w") as outfile:
        json.dump(data_dict, outfile, indent=4)

    display(f"Data saved to {filename}", verbosity=1)

# Entry point
if __name__ == "__main__":
    main()


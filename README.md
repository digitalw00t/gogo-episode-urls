---

# gogoanime-show_info.py

## Overview

`gogoanime-show_info.py` is a web scraping script designed to extract and analyze information about anime shows from the [Gogoanime website](https://gogoanime3.net/). It retrieves details such as the title, number of episodes, genre, status, type, released date, other names, and plot summary.

## Version

v0.1.4

## Requirements

- Python 3.x
- BeautifulSoup
- requests

## Installation

1. Install Python 3.x.
2. Install the required libraries using pip:

   ```bash
   pip install requests beautifulsoup4
   ```

## Usage

### Command-line Arguments

- `url_part`: The part of the URL to be scraped (e.g., "isekai-nonbiri-nouka-dub").
- `--debug`: Set the debug level (0: None, 1: Info, 2: Verbose, 3: Full HTML dump). Default is 0.

### Example

To scrape information for a specific anime, use the following command:

```bash
./gogoanime-show_info.py "isekai-nonbiri-nouka-dub" --debug 1
```

## Output

The extracted anime details are saved to a JSON file named `infodump.json`.

## Author

Draeician (2023-08017)

## Disclaimer

This script is intended for educational purposes only. Be mindful of the terms and conditions of the website being scraped and use this script responsibly.

---

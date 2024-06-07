# Sitemap Generator

This project is a simple web crawler and sitemap generator implemented in Python. It validates URLs, crawls websites up to a specified depth, and generates an XML sitemap containing the crawled URLs and their modification times (if available).

## Features

- Validates URLs to ensure they are correctly formatted.
- Crawls websites recursively, extracting and following links.
- Generates an XML sitemap of the crawled URLs.
- Respects `robots.txt` to avoid disallowed URLs.
- Attempts to fetch and include the last modification time of URLs in the sitemap.

## Requirements

- Python 3.x
- Required libraries: `urllib`, `beautifulsoup4`, `lxml`
- Project dependencies managed with Poetry

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/danielecammarata/py-sitemap-generator.git
    cd py-sitemap-generator
    ```

2. Install Poetry if you haven't already:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3. Install the project dependencies:
    ```bash
    poetry install
    ```

## Usage

Run the script and follow the prompts to enter a URL. The script will validate the URL, crawl the website, and generate a sitemap.

```python
python sitemap_generator.py

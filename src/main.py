import urllib.robotparser
import urllib.parse
from urllib.request import urlopen
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


def validate_url(url):
    """
    Validates the given URL format using urllib.parse.urlparse().

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """

    try:
        parsed_url = urllib.parse.urlparse(url)
        return all(
            [parsed_url.scheme, parsed_url.netloc]
        )  # Check for scheme and netloc
    except ValueError:
        return False


def crawl_website(url, max_depth=2, seen_urls=set()):
    """
    Crawls the website recursively, extracting links and adding them to the sitemap.

    Args:
        url (str): The URL to crawl.
        max_depth (int, optional): The maximum depth of recursion (default: 2).
        seen_urls (set, optional): A set to store visited URLs to avoid duplicates.

    Returns:
        list: A list of URLs found during crawling.
    """

    robots = urllib.robotparser.RobotFileParser()
    robots.set_url(f"{url}/robots.txt")
    robots.read()

    if not robots.can_fetch("*", url):
        print(f"Crawling disallowed by robots.txt for {url}")
        return []

    seen_urls.add(url)
    links = []

    try:
        response = urlopen(url)
        soup = BeautifulSoup(response, "lxml")

        # Extract links from anchor tags with valid href attributes
        for a in soup.find_all("a", href=True):
            link = a["href"]

            # Handle relative URLs
            if not urllib.parse.urlparse(link).netloc:
                link = urllib.parse.urljoin(url, link)

            # Only add unique URLs within the allowed domain
            if link not in seen_urls and link.startswith(url.split("/")[0] + "//"):
                seen_urls.add(link)
                links.append(link)

                if max_depth > 0:
                    links.extend(crawl_website(link, max_depth - 1, seen_urls))

    except Exception as e:
        print(f"Error crawling {url}: {e}")

    return links


def generate_sitemap(url, filename="sitemap.xml", max_depth=2):
    """
    Generates an XML sitemap containing the crawled URLs and their modification times (if available).

    Args:
        url (str): The starting URL for crawling.
        filename (str, optional): The filename of the sitemap (default: "sitemap.xml").
        max_depth (int, optional): The maximum depth of recursion (default: 2).
    """

    urls = crawl_website(url, max_depth)

    sitemap_xml = ET.Element(
        "urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
    )

    for url in urls:
        url_elem = ET.SubElement(sitemap_xml, "url")

        loc_elem = ET.SubElement(url_elem, "loc")
        loc_elem.text = url

        # Attempt to fetch modification time using HEAD request (optional)
        try:
            head_response = urlopen(url, method="HEAD")
            lastmod_elem = ET.SubElement(url_elem, "lastmod")
            lastmod_elem.text = head_response.getheader("Last-Modified")
        except Exception:
            pass  # Handle cases where Last-Modified header is unavailable

    with open(filename, "wb") as f:
        f.write(ET.tostring(sitemap_xml, encoding="utf-8", xml_declaration=True))

    print(f"Sitemap generated successfully: {filename}")


def start():
    while True:
        url = input("Enter a valid URL (or 'q' to quit): ")
        if url.lower() == "q":
            break

        if not validate_url(url):
            print(
                "Invalid URL. Please enter a valid format (e.g., https://some_url.com"
            )
        else:
            generate_sitemap(url)

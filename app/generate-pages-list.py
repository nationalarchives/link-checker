import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime

from lib.parse_html_page import get_links_from_page
from lib.parse_xml_sitemap import get_urls_from_sitemap

parser = argparse.ArgumentParser("simple_example")
parser.add_argument(
    "sitemap",
    help="The URL of an XML sitemap to itterate through.",
    type=str,
)
parser.add_argument(
    "-i",
    "--ignore",
    dest="ignore_list",
    action="append",
    help="Pages in the sitemap to ignore",
    required=False,
)
args = parser.parse_args()


pages = get_urls_from_sitemap(args.sitemap)
if args.ignore_list is not None:
    pages = [page for page in pages if page not in args.ignore_list]

links = set()
for page in pages:
    links.add(page)
    for link in get_links_from_page(page):
        links.add(link)

with open("links.txt", "w") as f:
    f.write("# LinkChecker URL list\n")
    f.write("\n".join(links))
sys.exit()

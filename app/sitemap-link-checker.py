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
    "url",
    help="The URL of an XML sitemap to itterate through.",
    type=str,
)
parser.add_argument(
    "-i",
    "--ignore",
    dest="ignore_list",
    action="append",
    help="Link URL to ignore",
    required=False,
)
args = parser.parse_args()


pages = get_urls_from_sitemap(args.url)
failed_links = []
checked_links = []

for page_url in pages:
    print()
    try:
        page_links = get_links_from_page(page_url)
    except Exception as e:
        print(f"⚠️ [ FAIL ] {page_url} - URLError: {e}")
    for link_url in page_links:
        if args.ignore_list is not None and link_url in args.ignore_list:
            print(f"🙈 [IGNORE] {link_url}")
        elif link_url in checked_links:
            print(f"🙈 [ DUPL ] {link_url}")
        else:
            checked_links.append(link_url)
            try:
                conn = urllib.request.urlopen(link_url)
            except urllib.error.HTTPError as e:
                print(f"❌ [ FAIL ] {link_url} - {e.code}")
                failed_links.append(
                    {"page": page_url, "link": link_url, "response": e.code}
                )
            except urllib.error.URLError as e:
                print(f"❌ [ FAIL ] {link_url} - {e.reason}")
                failed_links.append(
                    {"page": page_url, "link": link_url, "error": str(e.reason)}
                )
            else:
                print(f"✅ [ PASS ] {link_url}")


with open("report.json", "w") as f:
    now = datetime.now()
    json.dump(
        {
            "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "sitemap": args.url,
            "broken_links": failed_links,
        },
        f,
        ensure_ascii=False,
        indent=4,
    )

if len(failed_links):
    print()
    print(f"❌ [ FAIL ] {len(failed_links)}/{len(checked_links)} links failed")
    sys.exit(1)
else:
    print()
    print(f"✅ [ PASS ] {len(checked_links)} links passed")
    sys.exit()

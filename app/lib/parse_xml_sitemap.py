import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET


def get_urls_from_sitemap(sitemap_url):
    root = None
    pages = []

    try:
        with urllib.request.urlopen(sitemap_url) as f:
            xml = f.read().decode("utf-8")
            root = ET.fromstring(xml)
    except urllib.error.HTTPError as e:
        print(f"⚠️ [ FAIL ] {sitemap_url} - HTTPError: {e.code}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"⚠️ [ FAIL ] {sitemap_url} - URLError: {e.reason}")
        sys.exit(1)

    if root is not None:
        for url in root:
            for loc in url:
                if (
                    loc.tag
                    == "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
                ):
                    pages.append(loc.text)

    return pages

import re
import urllib.error
import urllib.request


def get_links_from_page(url):
    print(f"Getting links from {url}...")
    links = []
    try:
        with urllib.request.urlopen(url) as page:
            html = page.read().decode("utf-8")
            links = re.findall(r'<a[^>]*href="(http[^"]+)"', html)
    except urllib.error.HTTPError as e:
        raise Exception(f"HTTPError: {e.code}")
    except urllib.error.URLError as e:
        raise Exception(f"URLError: {e.reason}")
    return links

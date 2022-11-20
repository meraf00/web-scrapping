from bs4 import BeautifulSoup
import requests

seed = (
    'https://twins-furniture.vercel.app',
)


def get_urls(site):
    sites = set()

    try:
        response = requests.get(site)
    except:
        return sites

    if response.status_code != 200:
        return sites

    html = response.content
    soup = BeautifulSoup(html, 'lxml')

    a_tags = soup.find_all('a')
    for a_tag in a_tags:
        href = a_tag.get('href')

        if not href:
            continue

        if href.startswith('/'):
            href = site + href

        sites.add(href)

    return sites


def scrape(sites, depth=1):
    found = set()
    for site in sites:
        found = found.union(get_urls(site))

    if depth > 0:
        return found.union(scrape(found, depth - 1))

    return found


sc = scrape(seed)
print(sc, len(sc))

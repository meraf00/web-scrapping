import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def is_alive(url):
    try:
        return requests.get(url).status_code == 200
    except:
        return False


def get_urls(site):
    response = requests.get(site)
    
    parsed = BeautifulSoup(response.text, 'lxml')
    
    a_tags = parsed.find_all('a', href=True)
    
    links = set()
    for a_tag in a_tags:
        absolute_url = urljoin(site, a_tag['href'])
        if is_alive(absolute_url):
            links.add(absolute_url)
    
    return links


def scrape(seed_sites, depth=0):
    urls = set(seed_sites)
    for site in seed_sites:
        urls = urls.union(get_urls(site))

    unexplored = urls.difference(seed_sites)

    if depth > 0:
        return urls.union(scrape(unexplored, depth - 1) )

    return urls   
    


if __name__ == "__main__":
    seed_sites = (
        'https://twins-furniture.vercel.app/',
    )

    found_sites = scrape(seed_sites)

    print(found_sites)

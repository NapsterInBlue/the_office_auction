from datetime import datetime

import requests
from bs4 import BeautifulSoup

now = datetime.now()
TODAY = now.strftime('%Y%m%d')

BASE_URL = r'https://auction.screenbid.com/view-auctions/catalog/id/105/'


def get_no_verify(url):
    session = requests.Session()
    session.verify = False
    html = session.post(url=url).text

    return html

def save_raw_page(item_name, html):
    file_name = 'data/' + item_name + ' ' + TODAY + '.html'
    with open(file_name, 'w') as f:
        f.write(html)


def get_item_pages(soup):
    '''Finds all links to lot pages and returns tuples of
    (item name, URL)'''
    a_tags = soup.find_all('a', class_="auc-lot-link lot-title")
    return [(tag.text, tag.get('href')) for tag in a_tags]

def get_next_page_url(html):
    soup = BeautifulSoup(html, 'lxml')
    page_links = soup.find_all('span', class_='paginator')[0]
    next_page_tag = page_links.find_all('a')[-1]
    next_page_query_string = next_page_tag.get('href')
    next_page_url = BASE_URL + next_page_query_string

    return next_page_url


if __name__ == '__main__':
    html = get_no_verify(BASE_URL)
    soup = BeautifulSoup(html, 'lxml')

    item_pages = get_item_pages(soup)

    first_page = item_pages[0]

    first_page_name = first_page[0]
    first_page_html = get_no_verify(first_page[1])

    save_raw_page(first_page_name, first_page_html)

    print(get_next_page_url(html))

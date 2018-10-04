import requests
from bs4 import BeautifulSoup


BASE_URL = r'https://auction.screenbid.com/view-auctions/catalog/id/105/?page=1&sort=6&dir=1'


def get_no_verify(url):
    session = requests.Session()
    session.verify = False
    html = session.post(url=BASE_URL).text

    return html


def get_item_pages(soup):
    '''Finds all links to lot pages and returns tuples of
    (item name, URL)'''
    a_tags = soup.find_all('a', class_="auc-lot-link lot-title")
    return [(tag.text, tag.get('href')) for tag in a_tags]


def follow_page(a_tag):
    url = a_tag.get('href')
    html = get_no_verify(url)

    return html


if __name__ == '__main__':
    html = get_no_verify(BASE_URL)
    soup = BeautifulSoup(html, 'lxml')


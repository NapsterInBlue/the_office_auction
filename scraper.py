import requests
from bs4 import BeautifulSoup


BASE_URL = r'https://auction.screenbid.com/view-auctions/catalog/id/105/?page=1&sort=6&dir=1'


def get_no_verify(url):
    session = requests.Session()
    session.verify = False
    conn = session.post(url=BASE_URL)

    return conn


def get_item_pages(soup):
    return soup.find_all('a', class_="auc-lot-link lot-title")


def follow_page(a_tag):
    url = a_tag.get('href')


if __name__ == '__main__':
    conn = get_no_verify(BASE_URL)
    html = conn.text
    soup = BeautifulSoup(html, 'lxml')


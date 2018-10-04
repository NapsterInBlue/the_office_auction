import re
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from selenium import webdriver

now = datetime.now()
TODAY = now.strftime('%Y%m%d')

BASE_URL = r'https://auction.screenbid.com/view-auctions/catalog/id/105/'
AUCTION_URL = r'https://auction.screenbid.com/'


def get_no_verify(url):
    session = requests.Session()
    session.verify = False
    html = session.post(url=url).text

    return html

def clean_item_names(name):
    correct_chars = re.compile('[\w\s\d]', re.I)
    clean_name = ''.join(correct_chars.findall(name))
    return clean_name


def save_raw_page(item_name, html, extra=''):
    file_name = 'data/' + item_name + ' ' + extra + ' ' + TODAY + '.html'
    with open(file_name, 'w', encoding='utf-8') as f:
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

def get_item_bid_url(html):
    soup = BeautifulSoup(html, 'lxml')
    bid_query_string = (soup.find('span', id='bidHistory')
                            .find('a').get('href'))

    item_bid_url = AUCTION_URL + bid_query_string
    return item_bid_url

def save_item_bid_history(item_name, url):
    driver = webdriver.Chrome()
    driver.get(url)

    i = 1
    while True:
        html = driver.page_source
        save_raw_page(item_name, html, extra=('bids ' + str(i)))
        try:
            next_page = driver.find_element_by_link_text('Next')
            next_page.click()
            i += 1
        except:
            break

    driver.close()

def check_for_files(item_name):
    files = os.listdir('data')
    found_data = any([item_name in name for name in files])
    return found_data


if __name__ == '__main__':
    html = get_no_verify(BASE_URL)

    for i in range(11):
        soup = BeautifulSoup(html, 'lxml')

        item_pages = get_item_pages(soup)
        for page_name, page_url in item_pages:
            page_name = clean_item_names(page_name)
            if check_for_files(page_name):
                continue

            page_html = get_no_verify(page_url)
            save_raw_page(page_name, page_html)

            bid_url = get_item_bid_url(page_html)
            save_item_bid_history(page_name, bid_url)
        
        html = get_no_verify(get_next_page_url(html))

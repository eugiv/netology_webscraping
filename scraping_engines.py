import requests
import random

from fake_headers import Headers
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def cook_soup_requests(url_soup: str):
    head_gen = Headers(headers=True)
    response = requests.get(url_soup, headers=head_gen.generate())
    hot_soup = BeautifulSoup(response.text, 'lxml')
    return hot_soup


def request_scrap(keywords: str):
    url_init = f'https://hh.ru/search/vacancy?text={keywords}&area=1&area=2&items_on_page=20'
    soup_pages = cook_soup_requests(url_init)
    pages = list(soup_pages.find('div', class_='pager').text)
    pages = [x for x in pages if x.isdigit()]

    main_block_lst = []
    for page in pages:
        url = f'https://hh.ru/search/vacancy?text={keywords}&area=1&area=2&page={int(page)-1}&items_on_page=20'
        soup = cook_soup_requests(url)
        main_block = soup.find_all('div', class_='serp-item')
        main_block_lst.extend(main_block)

    return main_block_lst


def playwright_scrap(keywords: str):
    url_soup = 'https://hh.ru/search/vacancy?&area=1&area=2'
    with sync_playwright() as p:
        browser_mode = input('Do you prefer to see the progress on your screen? (y/n)?')

        if browser_mode == 'y':
            mode_browser = False
        elif browser_mode == 'n':
            mode_browser = True
        else:
            print("Ok, so if you want to mess up the choice will be random")
            mode_browser = random.choice([True, False])

        browser = p.firefox.launch(headless=mode_browser, slow_mo=2000)
        page = browser.new_page(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                                           '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        page.goto(url_soup, timeout=0)
        page.fill('#a11y-search-input', keywords)
        page.click('.supernova-search-group__submit > button:nth-child(1)')

        main_block_lst = []
        while True:
            html = page.inner_html('#HH-React-Root > div > div.HH-MainContent.HH-Supernova-MainContent')
            soup = BeautifulSoup(html, 'lxml')
            main_block = soup.find_all('div', class_='serp-item')
            main_block_lst.extend(main_block)
            if soup.find('a', {'data-qa': 'pager-next'}):
                page.click('#HH-React-Root > div > div.HH-MainContent.HH-Supernova-MainContent > '
                           'div.main-content.main-content_broad-spacing > div.bloko-columns-wrapper > '
                           'div.sticky-sidebar-and-content--NmOyAQ7IxIOkgRiBRSEg > div:nth-child(2) > '
                           'div:nth-child(1) > div > main > div.bloko-gap.bloko-gap_top > div > a')
            else:
                break

        return main_block_lst

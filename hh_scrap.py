import requests
from fake_headers import Headers
from bs4 import BeautifulSoup

head_gen = Headers(os='win', browser='chrome')

search_keywords = ["python", "flask", "django"]
search_keywords = "+".join(search_keywords)

url_init = f'https://hh.ru/search/vacancy?text={search_keywords}&area=1&area=2'


def cook_soup(url_soup: str):
    response = requests.get(url_soup, headers=head_gen.generate())
    html_pages = response.text
    hot_soup = BeautifulSoup(html_pages, 'lxml')
    return hot_soup


soup_pages = cook_soup(url_init)
pages = list(soup_pages.find('div', class_='pager').text)
pages = [x for x in pages if x.isdigit()]

for page in pages:
    url = f'https://hh.ru/search/vacancy?text={search_keywords}&area=1&area=2&page={int(page)-1}'
    soup = cook_soup(url)

    main_block = soup.find_all('div', class_='serp-item')

    for element in main_block:
        link = element.find('a')['href']
        print(link)




# if __name__ == "__main__":
#     search_formatter(search_keywords)

import requests
from fake_headers import Headers
from bs4 import BeautifulSoup

search_keywords = ["python", "flask", "django"]
search_keywords = "+".join(search_keywords)


def cook_soup(url_soup: str):
    head_gen = Headers(headers=True)

    response = requests.get(url_soup, headers=head_gen.generate())
    html = response.text
    hot_soup = BeautifulSoup(html, 'lxml')
    return hot_soup


url_init = f'https://hh.ru/search/vacancy?text={search_keywords}&area=1&area=2'

soup_pages = cook_soup(url_init)
pages = list(soup_pages.find('div', class_='pager').text)
pages = [x for x in pages if x.isdigit()]

for page in pages:
    url = f'https://hh.ru/search/vacancy?text={search_keywords}&area=1&area=2&page={int(page)-1}'
    print(url)
    soup = cook_soup(url)
    main_block = soup.find_all('div', class_='serp-item')

    count = 0
    for element in main_block:
        link = element.find('a')['href']
        count += 1
        print(link)
        print(count)




# if __name__ == "__main__":
#     search_formatter(search_keywords)

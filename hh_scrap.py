import re

import requests
from fake_headers import Headers

head_gen = Headers(os='win', browser='chrome')

search_keywords = ['flask', 'django']

url = f'https://hh.ru/search/vacancy?text=&area=1&area=2'

response = requests.get(url, headers=head_gen.generate())
print(response)

def search_formatter(search_list: list):
    
    search_pattern = r""


if __name__ == "__main__":
    search_formatter(search_keywords)

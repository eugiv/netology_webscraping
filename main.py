import os
import json

from scraping_engines import request_scrap as rs
from scraping_engines import playwright_scrap as pws
from hh_scrap_provider import data_processing as dp


if __name__ == '__main__':
    search_keywords = ["python", "flask", "django"]
    search_keywords_req = "+".join(search_keywords)
    search_keywords_pw = " ".join(search_keywords)

    current_dir = os.getcwd()
    path = os.path.join(current_dir, 'hh_scrap.json')

    engine_choice = input('Choose scraping engine: (1 - Requests, 2 - Playwright): ')

    if engine_choice == '1':
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(dp(rs(search_keywords_req)), f, ensure_ascii=False, indent=4)
            print('json file with scraped data has been dumped')

    elif engine_choice == '2':
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(dp(pws(search_keywords_pw)), f, ensure_ascii=False, indent=4)
            print('json file with scraped data has been dumped')
    else:
        print('Invalid choice. Please choose either 1 or 2. Try again.')

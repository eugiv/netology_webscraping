def elems_text_finder(html_element: str, html_tag: str, html_attrs: dict, lst_to_append: list):
    if html_element.find(html_tag, html_attrs):
        txt = html_element.find(html_tag, html_attrs).text
    else:
        txt = ''
    lst_to_append.append(txt)


def data_processing(main_html_data_block: str):
    link_lst = []
    salary_lst = []
    company_lst = []
    city_lst = []

    for element in main_html_data_block:
        if element.find('a')['href']:
            link = element.find('a')['href']
        else:
            link = 'no link provided'
        link_lst.append(link)

        elems_text_finder(element, 'span', {'class': 'bloko-header-section-2'}, salary_lst)
        elems_text_finder(element, 'a', {'data-qa': 'vacancy-serp__vacancy-employer'}, company_lst)
        elems_text_finder(element, 'div', {'data-qa': 'vacancy-serp__vacancy-address'}, city_lst)

    link_lst = [elem.split('?')[0].strip() for elem in link_lst]
    city_lst = [elem.split(',')[0].strip() for elem in city_lst]
    company_lst = [elem.replace('ООО\xa0', '').replace('АО\xa0', '') for elem in company_lst]
    currency_lst = [elem.split(' ')[-1] for elem in salary_lst]
    salary_lst = [elem.replace('\u202f', '').replace(' ₽', '') for elem in salary_lst]

    hh_scrap_data = {'Link': link_lst,
                     'Salary': salary_lst,
                     'Currency': currency_lst,
                     'Company': company_lst,
                     'City': city_lst}
    return hh_scrap_data

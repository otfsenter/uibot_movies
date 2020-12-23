import requests
from bs4 import BeautifulSoup
import config

from log import logger


def get_detail_link(page_url):
    url_name_list = []

    response = requests.get(page_url).content

    soup = BeautifulSoup(response, 'html.parser')
    div_content = soup.find('div', {'class': 'co_content8'})
    tables = div_content.find_all('table', {'class': 'tbspan'})

    for table in tables:
        tag_a = table.find('a')
        movie_url_suffix = tag_a.get('href')
        movie_name = tag_a.get_text().strip()
        url_name_list.append([movie_url_suffix, movie_name])

        # /html/gndy/dyzz/20201202/60782.html
        # 2020年剧情惊悚《让他走》BD中英双字幕

    return url_name_list


def get_page_url_list():
    page_url_list = []

    response = requests.get(config.start_urls).content

    soup = BeautifulSoup(response, 'html.parser')

    div_page = soup.find('select', {'name': 'sldd'})
    pages = div_page.find_all('option')

    for page in pages:
        url = page.get('value').strip()
        page_number = page.get_text().strip()
        page_url_list.append([page_number, url])

        # ['1', 'list_23_1.html'], ['2', 'list_23_2.html']

    return page_url_list


def main():
    page_url_list = get_page_url_list()
    for page, url in page_url_list:
        url_each_page = config.page_url_root + url

        logger.info(page)
        logger.info(url)
        logger.info(url_each_page)

        url_name_list = get_detail_link(url_each_page)
        for url_each_movie_suffix, movie_name in url_name_list:
            url_each_movie = config.one_movie_url_root + url_each_movie_suffix

            logger.info(url_each_movie)

            break
        break


if __name__ == '__main__':
    main()

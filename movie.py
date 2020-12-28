import re

import openpyxl as openpyxl
import requests
from bs4 import BeautifulSoup

import config
from log import logger

file_excel = 'movie.xlsx'

# 这些开头的不好分割成列表
all_in_one_list = [
    '发布时间',
    'imdb评分',
]

# 这些开头的描述不需要
not_usage_list = [
    '下载地址',
    '温馨提示',
    '下载方法',
    '点击进入',
]

# excel表头的标题
title_list = [
    "译名",
    "片名",
    "下载地址",
    "豆瓣评分",
    "豆瓣评分人数",
    "imdb评分",
    "imdb评分人数",
    "发布时间",
    "年代",
    "产地",
    "类别",
    "语言",
    "字幕",
    "上映日期",
    "文件格式",
    "视频尺寸",
    "片长",
    "导演",
    "编剧",
    "主演",
    "标签",
    "简介",

]

global_data_list = []

global_data_list.append(title_list)


def get_score_people_number(score_peopele_str):
    split_list = re.split('(from|users)', score_peopele_str)
    no_space_list = [i.strip() for i in split_list if i]

    score = no_space_list[0].split('/')[0]
    people_number = no_space_list[2]

    for i in [',', '.', '-']:
        score = str(score).replace(i, '')
        people_number = str(people_number).replace(i, '')

    return score, people_number


def get_data(no_space_content_list, magnet_link):
    """
    整理成可以直接写入excel的数据
    """
    data_dict = {}

    for nsc in no_space_content_list:

        # 每段前几个字符：年\u3000代\u3000，
        # 所以把正常的字符取出来
        nr_new_list = re.split('\u3000', nsc)

        # 如果列表个数大于3，就取第一个和第3个，组合成标题：年代、导演...
        if len(nr_new_list) > 3:
            title_each = nr_new_list[0] + nr_new_list[2]
            content_each = ' '.join(nr_new_list[3:])
            data_dict.setdefault(title_each, content_each)

        # 如果是两个，第一个就是标题，第二个是内容
        elif len(nr_new_list) == 2:
            title_each = nr_new_list[0]
            content_each = nr_new_list[1]

            # print('in 2: title_each', title_each)
            # print('in 2: content_each', content_each)

            if '豆瓣评分' in title_each:
                score, people_number = get_score_people_number(content_each)
                data_dict.setdefault('豆瓣评分', float(score))
                data_dict.setdefault('豆瓣评分人数', int(people_number))
            else:
                data_dict.setdefault(title_each, content_each)

        # 剩下的就是一个元素的，没有明显分隔符的
        else:
            for aio in all_in_one_list:
                total_single_str = str(nr_new_list[0].strip()).lower()
                aio_lower = str(aio).lower()

                if aio_lower in total_single_str:
                    title_each = aio_lower
                    content_each = total_single_str.replace(aio_lower, '').replace('：', '')

                    if 'imdb评分' in total_single_str:
                        score, people_number = get_score_people_number(content_each)
                        data_dict.setdefault('imdb评分', float(score))
                        data_dict.setdefault('imdb评分人数', int(people_number))


                    else:
                        data_dict.setdefault(title_each, content_each)

    # 下载地址
    data_dict.setdefault('下载地址', magnet_link)

    # 根据标题排序
    detail_data_list = []
    for title in title_list:
        detail_data_list.append(data_dict.get(title))

    global_data_list.append(detail_data_list)


def get_html_content(url_each_movie):
    """
    把详情页的数据爬下来，整理成没有空行的列表

    :return: 返回没有空行的列表
    """
    # 从详情页面把电影所有信息爬下来
    # url_movie = 'https://www.dytt8.net/html/gndy/dyzz/20201220/60866.html'
    response = requests.get(url_each_movie).content
    soup = BeautifulSoup(response, 'html.parser')
    div_content = soup.find('div', {'class': 'co_content8'})

    if div_content:
        magnet_link = div_content.find('a').get('href')
        # 把字符串进行解码，转换成列表
        content = div_content.get_text().strip()
        content_decode = content.encode('latin-1', 'ignore').decode('gb2312', 'ignore')
        content_list = re.split('[\n◎]', content_decode)

        # 去掉空行
        no_space_content_list = []
        for c in content_list:
            if c.strip():
                no_space_content_list.append(c)

        return [no_space_content_list, magnet_link]
    else:
        return False




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


def to_excel(data_list):
    data_list = list(data_list)

    wb = openpyxl.Workbook()
    ws = wb.active

    for row_index, row_list in enumerate(data_list):
        row_index = row_index + 1

        for col_index, cell_value in enumerate(row_list):
            col_index = col_index + 1

            ws.cell(row=row_index, column=col_index, value=cell_value)

    wb.save(file_excel)


def main():
    page_url_list = get_page_url_list()
    for page, url in page_url_list[:2]:
        url_each_page = config.page_url_root + url

        logger.info(page)
        logger.info(url)
        logger.info(url_each_page)

        url_name_list = get_detail_link(url_each_page)
        for url_each_movie_suffix, movie_name in url_name_list:
            url_each_movie = config.one_movie_url_root + url_each_movie_suffix

            html_content = get_html_content(url_each_movie)
            if html_content:
                no_space_content_list, magnet_link = html_content
                get_data(no_space_content_list, magnet_link)

                logger.info(url_each_movie)

    # TODO: 数据有问题，标题很多空白
    # TODO： 把左边小框的数据也爬了，不要爬

    to_excel(global_data_list)


if __name__ == '__main__':
    main()

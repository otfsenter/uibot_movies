
import time
import requests
from bs4 import  BeautifulSoup
from log import logger


#class NewestMovieSpider():
    #name = 'newest_movie'
    #allowed_domains = ['www.dytt8.net']
    ## 从该urls列表开始爬取
    #start_urls = ['http://www.dytt8.net/html/gndy/dyzz/']
    #start_urls = 'http://www.dytt8.net/html/gndy/dyzz/'
    #tree = requests.get(start_urls).text

    #def get_hash(self, data):
    #    md5 = hashlib.md5()
    #    md5.update(data.encode('utf-8'))
    #    return md5.hexdigest()

def parse():
    start_urls = 'http://www.dytt8.net/html/gndy/dyzz/'
    response = requests.get(start_urls).text

    logger.info(str(response))

    domain = "https://www.dytt8.net"

    # 解析
    # tree = etree.HTML(response)
    soup = BeautifulSoup(response)



    # 爬取下一页
    #last_page_num = tree.xpath('//select[@name="sldd"]//option[last()]/text()').extract()[0]
    last_page_num = tree.xpath('//select[@name="sldd"]//option[last()]/text()')[0]
    soup.find
    #print(last_page_num)
    last_page_url = 'list_23_' + last_page_num + '.html'
    #print(last_page_url)
    next_page_url = tree.xpath('//div[@class="x"]//a[last() - 1]/@href')[0]
    #print(next_page_url)
    #next_page_num = next_page_url.split('_')[-1].split('.')[0]
    next_page_num = next_page_url.split('_')[-1].split('.')[0]
    #print(last_page_num)
    if next_page_url != last_page_url:
        url = 'https://www.dytt8.net/html/gndy/dyzz/' + next_page_url
        #print(url)
        logging.log(logging.INFO, f'***************** crawling page {next_page_num} ***************** ')
        #yield parse()
        #yield Request(url=url, callback=parse, meta={'item': item}, dont_filter = True)

    # 爬取详情页
    urls = tree.xpath('//b/a/@href')   #  list type
    #print('urls', urls)
    for url in urls:
        url = domain + url
        #print(url)
        parse_single_page(tree, url)
        #yield Request(url=url, callback=parse_single_page, meta={'item': item}, dont_filter = False)

def parse_single_page(tree, url):
    # 适配不同html结构的电影详情页
    detail_xpath_list = [
                            '//div[@id="Zoom"]//p/text()',
                            '//div[@id="Zoom"]//td/text()',
                            '//div[@id="read_tpc"]/text()',
                        ]
    #item = tree.meta['item']
    #item['movie_link'] = tree.url
    #logging.log(logging.INFO, 'crawling url: ' + item['movie_link'])
    # 电影天堂的前端太坑，写了这么多不同结构的html，所以就会导致报错获取不到详细内容，以下对不同html结构适配。 
    for detail_xpath in detail_xpath_list:
        print(detail_xpath)
        detail_row = tree.xpath(detail_xpath)		# str type list
        print(detail_row)
        #print('lasjflsafjlsadfjsla' + detail_row)
        #logging.log(logging.INFO, f'*************** detail_row: {detail_row} ****************')
        #logging.log(logging.INFO, f'*************** detail_row len: {len(detail_row)} ****************')
        if len(detail_row) > 4:
            #logging.log(logging.INFO, f'********** movie detail from {detail_xpath} **********')
            print(type(detail_row))
            print(detail_row)
            break

    # 将网页提取的str列表类型数据转成一个长字符串, 以圆圈为分隔符，精确提取各个字段具体内容
    detail_str = ''.join(detail_row)
    # 将电影详细内容hash，以过滤相同内容
    #item['movie_hash'] = get_hash(detail_str)
    #print(detail_str)
    #logging.log(logging.INFO, f"movie hash is: {item['movie_hash']}")
    detail_list = ''.join(detail_str).split('◎')

    logging.log(logging.INFO, '**************** movie detail log ****************')
    #item['movie_name'] = detail_list[1][5:].replace(6*u'\u3000', u', ')
    #logging.log(logging.INFO, 'movie_link: ' + item['movie_link'])
    #logging.log(logging.INFO, 'movie_name: ' + item['movie_name'])
    # 找到包含特定字符到字段
    for field in detail_list:
        if '主\u3000\u3000演' in field:
            # 将字段包含杂质去掉[5:].replace(6*u'\u3000', u', ')
            #item['movie_actors'] = field[5:].replace(6*u'\u3000', u', ')
            #logging.log(logging.INFO, 'movie_actors: ' + item['movie_actors'])
            logging.log(logging.INFO, 'movie_actors:')
        if '导\u3000\u3000演' in field:
            #item['movie_director'] = field[5:].replace(6*u'\u3000', u', ')
            #logging.log(logging.INFO, 'movie_directors: ' + item['movie_director'])
            logging.log(logging.INFO, 'movie_actors:')
        if '上映日期' in field:
            #item['movie_publish_date'] = field[5:].replace(6*u'\u3000', u', ')
            #logging.log(logging.INFO, 'movie_publish_date: ' + item['movie_publish_date'])
            logging.log(logging.INFO, 'movie_actors:')
        if '豆瓣评分' in field:
            #item['movie_score'] = field[5:].replace(6*u'\u3000', u', ')
            #logging.log(logging.INFO, 'movie_score: ' + item['movie_score'])
            logging.log(logging.INFO, 'movie_actors:')

    # 此处获取的是迅雷磁力链接，安装好迅雷，复制该链接到浏览器地址栏迅雷会自动打开下载链接，个别网页结构不一致会获取不到链接
    try:
        #item['movie_download_link'] = ''.join(tree.xpath('//p/a/@href'))
        #logging.log(logging.INFO, 'movie_download_link: ' + item['movie_download_link'])
        logging.log(logging.INFO, 'movie_actors:')
    except Exception as e:
        #item['movie_download_link'] = tree.url
        logging.log(logging.WARNING, e)
    #yield item

parse()
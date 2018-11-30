import random
import requests
from lxml import etree
from requests.exceptions import ConnectionError
from cookiespool.db import *


class ValidTester(object):
    def __init__(self, website='default'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)
    
    def test(self, headers):
        raise NotImplementedError
    
    def run(self):
        cookies_groups = self.cookies_db.all()
        for headers in cookies_groups:
            self.test(headers)


# 百姓网Cookie检测
class BaixingValidTester(ValidTester):
    def __init__(self, website='baixing'):
        ValidTester.__init__(self, website)
    
    def test(self, headers):
        print('正在测试--百姓网--Cookies',headers)
        try:
            test_url = TEST_URL_MAP[self.website]
            test_response = requests.get(url=test_url, headers=json.loads(headers))
            test_html = etree.HTML(test_response.text)
            if test_html.xpath('//span[@class="username"]/text()'):
                print('cookie可用')
            else:
                print('cookie失效')
                self.cookies_db.delete(json.dumps(headers))
                print('删除Cookies',headers)
        except ConnectionError as e:
            print('发生异常', e.args)


# 优信二手车Cookie检测
class YouxinValidTester(ValidTester):
    def __init__(self, website='youxin'):
        ValidTester.__init__(self, website)

    def test(self, headers):
        print('正在测试--优信二手车--Cookies', headers)
        try:
            page = random.randint(1, 50)
            listpage_url = 'https://www.xin.com/shanghai/i{}/'.format(page)
            response = requests.get(url=listpage_url, headers=json.loads(headers))
            html = etree.HTML(response.text)
            detail_url_list = html.xpath('//li[@class="con caritem conHeight"]')
            test_url = 'https:' + detail_url_list[random.randint(0, 39)].xpath('.//h2/span/@href')[0]
            test_response = requests.get(url=test_url, headers=json.loads(headers))
            test_html = etree.HTML(test_response.text)
            if test_html.xpath('//tr/td/span[@class="cd_m_pop_pics_desc_val"]/text()'):
                print('cookie可用')
            else:
                print('cookie失效')
                self.cookies_db.delete(json.dumps(headers))
                print('删除Cookies',headers)
        except ConnectionError as e:
            print('发生异常', e.args)


if __name__ == '__main__':
    YouxinValidTester().run()

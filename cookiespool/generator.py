import json
from cookiespool.db import RedisClient
import requests, time, random
from fake_useragent import UserAgent
import urllib3
from lxml import etree
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning


class CookiesGenerator(object):
    def __init__(self, website='default'):

        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)
    
    def new_cookies(self, *args):

        raise NotImplementedError

    def run(self):

        accounts_usernames = self.accounts_db.usernames()

        for username in accounts_usernames:

            if username:
                password = self.accounts_db.get(username)
                print('正在生成Cookies', '账号', username, '密码', password)
                result = self.new_cookies(username, password)
            else:
                print('正在生成Cookies')
                result = self.new_cookies()
            # 成功获取
            if result.get('status') == 1:
                content_data = result.get('content')
                print('成功获取到随机请求头', content_data)
                if self.cookies_db.set(username, content_data):
                    print('成功保存随机请求头')
            # 密码错误，移除账号
            elif result.get('status') == 2:
                print(result.get('content'))
                if self.accounts_db.delete(username):
                    print('成功删除账号')
            else:
                print(result.get('content'))


# 百姓网cookie获取
class BaixingCookiesGenerator(CookiesGenerator):

    def __init__(self, website='baixing'):
        CookiesGenerator.__init__(self, website)
        self.website = website
        self.url = 'http://www.baixing.com/oz/login?redirect=http%3A%2F%2Fwww.baixing.com%2Fw%2F'
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random
        }
    
    def new_cookies(self, *args):
        username = args[0]
        password = args[1]
        response = requests.get(url=self.url, headers=self.headers)

        html = etree.HTML(response.text)

        token = html.xpath('//input[@name="token"]/@value')[0]
        key = html.xpath('//input[@name="8cb44b44cba8fde"]/@value')[0]

        # 获取登录页面响应返回的cookie
        trackid = requests.utils.dict_from_cookiejar(response.cookies)['__trackId']
        uuid = requests.utils.dict_from_cookiejar(response.cookies)['__uuid']

        # 生成登录cookie
        cookie = '__trackId={};__city=shanghai;_alertkey=1;__uuid={};login_on_tab=0;_auth_redirect=http%3A%2F%2Fwww.baixing.com%2Fw%2F;'.format(
            trackid, uuid)

        # 关键参数
        login_url = 'http://www.baixing.com/oz/login?redirect=http%3A%2F%2Fwww.baixing.com%2Fw%2F'
        headers = {
            'User-Agent': self.ua.random,
            'Cookie': cookie,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'www.baixing.com',
            'Origin': 'http://www.baixing.com',
            'Referer': 'http://www.baixing.com/oz/login?redirect=http%3A%2F%2Fwww.baixing.com%2Fw%2F',
            'Upgrade-Insecure-Requests': '1'
        }
        data = {
            'identity': username,
            'password': password,
            'token': token,
            '8cb44b44cba8fde': key
        }
        response_login = requests.post(url=login_url, data=data, headers=headers)

        # 获取cookie参数
        t = requests.utils.dict_from_cookiejar(response_login.request._cookies)['__t']
        c = requests.utils.dict_from_cookiejar(response_login.request._cookies)['__c']
        u = requests.utils.dict_from_cookiejar(response_login.request._cookies)['__u']
        mui = requests.utils.dict_from_cookiejar(response_login.request._cookies)['mui']

        # 生成最终cookie
        login_cookie = '__trackId={};' \
                       '__uuid={};' \
                       'login_on_tab=0;' \
                       '__city=shanghai;' \
                       '_alertkey=1;' \
                       '__sense_session_pv=1;' \
                       '__t={};' \
                       '__u={};' \
                       '__c={};' \
                       '__n=user_6988538;' \
                       '__m=18721918121;mui={}'.format(trackid, uuid, t, u, c, mui)

        # 生成最终请求头
        baixing_data = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': self.ua.random,
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': login_cookie
        }
        return {
            'status': 1,
            'content': json.dumps(baixing_data)
        }


# 优信二手车cookie获取
class YouxinCookiesGenerator(CookiesGenerator):

    def __init__(self, website='youxin'):
        CookiesGenerator.__init__(self, website)
        self.number = 1
        self.new_session_xin = 'it9lijr12ct9peakob8rbmgnmumc7r01'
        self.anti_uid = '49697DDF-ACF1-9F19-DA7B-83EABF07131B'
        urllib3.disable_warnings(InsecureRequestWarning)
        urllib3.disable_warnings(InsecurePlatformWarning)
        self.ua = UserAgent()

    def get_uid(self):
        tm = str(time.time()).split('.')[0]
        url = 'https://www.xin.com/shanghai/i{}/'.format(random.randint(1, 51))
        headers = {
            'User-Agent': self.ua.random,
            'Host': 'www.xin.com',
            'Cookie': 'RELEASE_KEY=; '
                      'XIN_bhv_oc=5066; '
                      'XIN_anti_uid={}; '
                      'XIN_LOCATION_CITY=%7B%22cityid%22%3A%222401%22%2C%22areaid%22%3A%226%22%2C%22big_areaid%22%3A%221%22%2C%22provinceid%22%3A%2224%22%2C%22cityname%22%3A%22%5Cu4e0a%5Cu6d77%22%2C%22ename%22%3A%22shanghai%22%2C%22shortname%22%3A%22SH%22%2C%22service%22%3A%221%22%2C%22near%22%3A%22604%2C3001%2C101%2C2101%2C2118%2C2117%2C1501%2C3002%2C1502%2C1201%22%2C%22tianrun_code%22%3A%22021%22%2C%22zhigou%22%3A%221%22%2C%22longitude%22%3A%22121.4737010%22%2C%22latitude%22%3A%2231.2304160%22%2C%22city_rank%22%3A100%2C%22city_group%22%3A%223%22%2C%22is_gold_partner%22%3A%22-1%22%2C%22direct_rent_support%22%3A%221%22%2C%22salvaged_support%22%3A%221%22%2C%22isshow_c%22%3A%221%22%2C%22is_lease_back%22%3A%221%22%2C%22mortgage_service_fee%22%3A%2290000%22%2C%22is_small_pub_house%22%3A%220%22%2C%22is_wz_mortgage%22%3A%220%22%2C%22is_login%22%3A1%7D; NSC_20.eqppmxfc.yjo.dpn=ffffffffaf18140345525d5f4f58455e445a4a423660; '
                      'XIN_UID_CK=5e21beea-146c-a405-2a32-2df07fc0eac9; '
                      'Hm_lvt_ae57612a280420ca44598b857c8a9712=1530510447; '
                      'Hm_lpvt_ae57612a280420ca44598b857c8a9712={}; '
                      'session_xin={}; '
                      'SEO_REF=https://www.xin.com/shanghai/'.format(self.anti_uid, tm, self.new_session_xin)
        }

        response = requests.get(url, headers=headers, verify=False)

        uid = response.cookies.get('XIN_anti_uid', '')
        if uid:
            print('uid= ', uid)
            self.anti_uid = uid

    def get_session_xin(self):
        headers = {
            'User-Agent': self.ua.random,
            'Host': 'www.xin.com',
            'Cookie': 'XIN_bhv_oc=1233; '
                      'XIN_anti_uid={}; '
                      'XIN_LOCATION_CITY=%7B%22cityid%22%3A%221001%22%2C%22areaid%22%3A%224%22%2C%22big_areaid%22%3A%222%22%2C%22provinceid%22%3A%2210%22%2C%22cityname%22%3A%22%5Cu90d1%5Cu5dde%22%2C%22ename%22%3A%22zhengzhou%22%2C%22shortname%22%3A%22ZN%22%2C%22service%22%3A%221%22%2C%22near%22%3A%22201%2C501%2C2101%2C2117%2C1010%2C1002%2C601%2C2401%2C901%2C1201%22%2C%22tianrun_code%22%3A%220371%22%2C%22zhigou%22%3A%221%22%2C%22longitude%22%3A%22113.6253680%22%2C%22latitude%22%3A%2234.7465990%22%2C%22direct_rent_support%22%3A%221%22%2C%22salvaged_support%22%3A%221%22%2C%22isshow_c%22%3A%221%22%7D; '
                      'uid=rBAKEls5vG1giwDiR4LWAg==; '
                      'NSC_20.eqppmxfc.yjo.dpn=ffffffffaf18140345525d5f4f58455e445a4a423660; '
                      'XIN_UID_CK=5e21beea-146c-a405-2a32-2df07fc0eac9'.format(self.anti_uid)
        }

        response = requests.get('https://www.xin.com/search/get_wishlist_token', headers=headers, verify=False)
        # 从响应头的Set-Cookie中，取出session_xin
        session_xin = response.cookies.get('session_xin', '没有')
        return session_xin

    def new_cookies(self, *args):
        number_list = [1525 + self.number, 1319 + self.number, 1262 + self.number, 1436 + self.number, 1561 + self.number, 1452 + self.number,
                       1618 + self.number, 1624 + self.number, 1632 + self.number, 1631 + self.number, 1646 + self.number, 1742 + self.number,
                       1814 + self.number, 1891 + self.number, 1847 + self.number, 2286 + self.number]
        tm = str(time.time()).split('.')[0]

        # 每次请求详情页数据之前，需要判断number的值，目的就是爬取详情页几条数据之后，更换session_xin的值
        if self.number % 9 == 0:
            self.number += 1
            self.new_session_xin = self.get_session_xin()
            return

        headers = {
            'User-Agent': self.ua.random,
            'Host': 'www.xin.com',
            'Cookie': 'RELEASE_KEY=; '
                      'XIN_bhv_oc={}; '
                      'XIN_anti_uid={}; '
                      'XIN_LOCATION_CITY=%7B%22cityid%22%3A%221001%22%2C%22areaid%22%3A%224%22%2C%22big_areaid%22%3A%222%22%2C%22provinceid%22%3A%2210%22%2C%22cityname%22%3A%22%5Cu90d1%5Cu5dde%22%2C%22ename%22%3A%22zhengzhou%22%2C%22shortname%22%3A%22ZN%22%2C%22service%22%3A%221%22%2C%22near%22%3A%22201%2C501%2C2101%2C2117%2C1010%2C1002%2C601%2C2401%2C901%2C1201%22%2C%22tianrun_code%22%3A%220371%22%2C%22zhigou%22%3A%221%22%2C%22longitude%22%3A%22113.6253680%22%2C%22latitude%22%3A%2234.7465990%22%2C%22direct_rent_support%22%3A%221%22%2C%22salvaged_support%22%3A%221%22%2C%22isshow_c%22%3A%221%22%7D; '
                      'uid=rBAKEls5vG1giwDiR4LWAg==; '
                      'NSC_20.eqppmxfc.yjo.dpn=ffffffffaf18140345525d5f4f58455e445a4a423660; '
                      'XIN_UID_CK=5e21beea-146c-a405-2a32-2df07fc0eac9; '
                      'Hm_lvt_ae57612a280420ca44598b857c8a9712=1530510447; '
                      'Hm_lpvt_ae57612a280420ca44598b857c8a9712={}; '
                      'session_xin={}; '
                      'SEO_REF=https://www.xin.com/shanghai/; '
                      'XIN_CARBROWSE_IDS=%5B34630115%2C63182276%2C43369790%2C71613690%2C42020178%2C58264933%2C26738142%5D; '
                      'XIN_bhv_pc={}; '
                      'XIN_bhv_expires=1543475548992'.format(random.choice(number_list), self.anti_uid, tm, self.new_session_xin,
                                                             self.number)
        }
        self.number += 1
        print(headers)
        return {
            'status': 1,
            'content': json.dumps(headers)
        }

if __name__ == '__main__':
    generator = YouxinCookiesGenerator()
    generator.run()

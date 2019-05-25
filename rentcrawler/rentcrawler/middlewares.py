# 设置随机的USER-AGENT
import random
import logging
import requests

'''
    User-Agent
'''
class RandomUserAgentMiddleware():
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
            'Mozilla/5.0 (X11; Ubantu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2',
        ]
        # self.proxys = [
        #     '178.128.56.18:3128',
        #     '178.128.56.18:31',
        #     '167.99.63.67:8888',
        #     '183.173.110.231:1080',
        #     '58.244.192.5:8080'
        # ]

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agents)
        # print('当前使用的User-Agent为：' + str(request.headers['User-Agent']))
        # print('当前使用的Proxy为：' + str(random.choice(self.proxys)))

    def process_response(self, request, response, spider):
        response.status = 201
        return response

'''
    代理池
'''
class ProxyMiddleware():
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        if request.meta.get('retry_times'):
            proxy = self.get_random_proxy()
            if proxy:
                uri = 'https://{proxy}'.format(proxy=proxy)
                self.logger.debug('使用代理 ' + proxy)
                print('正在使用代理：' + proxy)
                request.meta['proxy'] = uri

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )



import requests
from lxml.html import fromstring
import traceback
from itertools import cycle


def Get_Proxy(link):
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()

    for i in parser.xpath('//tbody/tr'):
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)




    Proxy_Pool = cycle(proxies)
    for i in range(len(proxies)):
        proxy = next(Proxy_Pool)
        try:
            response = requests.get(url = link, proxies = {"https":proxy , "http":proxy})
            return proxy

        except:
            proxies.remove(proxy)


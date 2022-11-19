import re
import time

import requests

from utils import getlocalip, print_err, print_inf, print_suc

r_out = ''


def gethttpips(num: int):
    global r_out
    try:
        ip = '139.215.45.18'
        step0 = requests.get(
            url='https://wapi.http.linkudp.com/index/index/get_my_balance?neek=2137293&appkey=ced93afdcbe43be6f73cc62819467613').text
        print_inf('余额%s元' % re.findall('"balance":(.*?)}', step0)[0])
        time.sleep(3)
        step1 = requests.get(
            url='https://wapi.http.linkudp.com/index/index/save_white?neek=2137293&appkey=ced93afdcbe43be6f73cc62819467613&white=%s' % ip).text  # 加白
        print_suc(re.findall('"msg":"(.*?)"', step1)[0])
        time.sleep(1)
        step2 = requests.get(
            url='http://webapi.http.zhimacangku.com/getip?num=%s&type=1&pro=&city=0&yys=0&port=1&time=2&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=' % str(
                num)).text  # get
        r = step2.split('\n')
        if r is not None:
            for it in r:  # 逐行
                if len(it) > 10:
                    # it = it.replace(':', ' ')
                    # r_out += 'http %s' % it
                    it = it.replace(':',' ')
                    print('http %s' % it)
        open('proxy_output.txt', 'w+').write(r_out)

    except:
        print_err('get proxies from pool err')


def getsocks5ips(num: int):
    global r_out
    try:
        # ip = getlocalip()
        ip = '139.215.46.247'
        step0 = requests.get(
            url='https://wapi.http.linkudp.com/index/index/get_my_balance?neek=2137293&appkey=ced93afdcbe43be6f73cc62819467613').text
        print_inf('余额%s元' % re.findall('"balance":(.*?)}', step0)[0])
        time.sleep(3)
        step1 = requests.get(
            url='https://wapi.http.linkudp.com/index/index/save_white?neek=2137293&appkey=ced93afdcbe43be6f73cc62819467613&white=%s' % ip).text  # 加白
        print_suc(re.findall('"msg":"(.*?)"', step1)[0])
        time.sleep(1)
        step2 = requests.get(
            url='http://webapi.http.zhimacangku.com/getip?num=%s&type=1&pro=&city=0&yys=0&port=2&time=2&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=' % str(
                num)).text  # get
        r = step2.split('\n')
        if r is not None:
            for it in r:  # 逐行
                if len(it) > 10:
                    it = it.replace(':', ' ')
                    r_out += 'socks5 %s' % it
                    print('socks5 %s' % it)
        open('proxy_output.txt', 'w+').write(r_out)

    except:
        print_err('get proxies from pool err')


# https://wapi.http.linkudp.com/index/index/save_white?neek=2137293&appkey=ced93afdcbe43be6f73cc62819467613&white=您的ip
# http://webapi.http.zhimacangku.com/getip?num=10&type=1&pro=&city=0&yys=0&port=1&time=2&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=
gethttpips(100)

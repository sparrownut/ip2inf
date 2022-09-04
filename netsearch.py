# coding=utf-8
import re
import time

import ddddocr
import requests
from colorama import init

from config import args
from utils import print_inf, print_err, getproxy, generate_random_str, print_suc, blue

init(autoreset=True)
prox = getproxy()


def setcookies(text):
    cok = {}
    for it in re.findall('\'Set-Cookie\'\: \'(.*?);', str(text)):
        cok[str(it).split('=')[0]] = str(it).split('=')[1]
    return cok


def getsessionid():
    res = requests.get('https://sgk66.cc/login.html')
    return setcookies(res.headers)


def sgkreg():
    cookies = getsessionid()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-Exchange;v=b3;q=0.9: ',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/103.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    global prox
    una = generate_random_str(8)
    pwd = generate_random_str(8)

    retus = {}

    while True:
        captcha = requests.get(url='https://sgk66.cc/SCaptcha', cookies=cookies, headers=headers, proxies=prox).content
        ocr = ddddocr.DdddOcr()
        ocr_res = ocr.classification(captcha)
        data = {'username': una,
                'pass': pwd,
                'confirmPass': pwd,
                'code': ocr_res,
                'submit': '%E6%B3%A8%E5%86%8C'}
        url = 'https://sgk66.cc/rg.html'
        res = requests.post(url, cookies=cookies, headers=headers, data=data, proxies=prox)
        if '验证码输入错误' not in res.text and len(res.text) != 0:
            print_suc('社工库临时注册成功 una:' + una + ' pwd:' + pwd)
            retus['cookies'] = cookies
            retus['username'] = una
            retus['pass'] = pwd
            retus['headers'] = headers
            break
        # prox = getproxy()

    return retus


def sgklogin(una, pwd, headers, cookies):
    url = 'https://sgk66.cc/'
    while True:
        captcha = requests.get(url='https://sgk66.cc/SCaptcha', cookies=cookies, headers=headers, proxies=prox).content
        ocr = ddddocr.DdddOcr()
        ocr_res = ocr.classification(captcha)
        data = {'username': una,
                'pass': pwd,
                'code': ocr_res}
        res = requests.post(url + 'lg.html', cookies=cookies, headers=headers, data=data, proxies=prox)
        if '验证码输入错误' not in res.text and len(res.text) != 0:
            if '密码错误' in res.text:
                print_err('密码错误')
                return None
            print_suc('登录成功')
            return res.cookies


def sgksearch(text_query):
    swi = ''
    if not args.y:
        swi = input(blue('是否将搜集到的数据导入社工库查询? Y/N : '))
    if swi.upper() == 'Y' or swi == '':
        while True:
            try:
                r = sgksearch_unf(text_query)
                return r
            except Exception:
                print_err('连接社工库时网络出现错误，3s后重连')
                time.sleep(3)
    elif swi.upper() == 'N':
        pass
    else:
        print_err('输入参数错误')


def sgksearch_unf(text_query):
    r = ''
    sreg = sgkreg()
    sgklogin(una=sreg['username'], pwd=sreg['pass'], headers=sreg['headers'], cookies=sreg['cookies'])
    sreg['cookies']['n'] = sreg['username']
    print_inf('将搜索' + str(len(text_query)) + '条信息')
    ic = 0
    for text in text_query:
        ic += 1
        text_query.remove(text)
        if '@' in text:
            text = str(text).split('@')[0]
        if ic >= 6:  # 有次数限制了 换账号
            print_inf('查询次数到限制 切换账号')
            r += sgksearch(text_query)
            return r
        else:
            seres = requests.post(url='https://sgk66.cc/search.html', headers=sreg['headers'],
                                  data={'keyword': str(text), 'radiobutton': 'laomi'}, cookies=sreg['cookies'],
                                  proxies=prox)

            re_seres = re.findall('<div>(.*?)</div>', seres.text)
            i = 0

            lis = ['id', '昵称', '账号', '密码明文', '密码md5', '密码md5_2', 'salt', 'email', 'ip', '姓名', '性别',
                   '生日', '手机', '身份证',
                   '地址',
                   '户口', '公司', '大学', '专业', '学历', '省份', '城市', '电话', '其他']
            for it in re_seres:
                if 23 <= i < 47:
                    if str(it) != '1' and str(it) != '其他' and it != '':
                        print_suc(lis[i - 24] + ':' + str(it))
                        r += lis[i - 24] + ':' + str(it) + '\n'
                i += 1

    return r


def sgksearch_up(text_query, una, pwd):
    r = ''
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-Exchange;v=b3;q=0.9: ',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/103.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    cookie = getsessionid()
    sgklogin(una=una, pwd=pwd, headers=headers, cookies=cookie)
    cookie['n'] = una
    for text in text_query:
        if '@' in text:
            text = str(text).split('@')[0]
        seres = requests.post(url='https://sgk66.cc/search.html', headers=headers,
                              data={'keyword': str(text), 'radiobutton': 'laomi'}, cookies=cookie,
                              proxies=prox)
        re_seres = re.findall('<div>(.*?)</div>', seres.text)
        i = 0
        list = ['id', '昵称', '账号', '密码明文', '密码md5', '密码md5_2', 'salt', 'email', 'ip', '姓名', '性别', '生日',
                '手机', '身份证',
                '地址',
                '户口', '公司', '大学', '专业', '学历', '省份', '城市', '电话', '其他']
        for it in re_seres:
            if 23 <= i < 47:
                if str(it) != '1' and str(it) != '其他' and it != '':
                    print_suc(list[i - 24] + ':' + str(it))
                    r += list[i - 24] + ':' + str(it) + '\n'
            i += 1
    return r

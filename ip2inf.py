#!/usr/bin/python3
# coding=utf-8
import datetime
import os.path
import re
import threading
import time
import traceback

import requests
import shodan
import whois
from colorama import init
from shodan import APIError

from config import args, threadcou
from data_struct.ip2infres import ip2infres
from exp.fish.fishserver import startserv
from netsearch import sgksearch
from portinf import scan
from utils import print_err, print_inf, print_suc, init_headers, getproxy, check_ip, red, resolve_domain, blue, \
    getlocalip

debug = False
init(autoreset=True)
"""
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-User': '?1',
'Sec-Fetch-Dest': 'document',
'Referer': 'https://site.ip138.com/192.186.1.2/',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'close'
"""


def getactLoc(ip):
    loc = {
        'jing': '',
        'wei': ''
    }
    url = 'http://tool.liumingye.cn/ip/?ip=%s' % ip
    headers = {'Accept': 'text/html, */*; q=0.01',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest',
               'Referer': 'http://tool.liumingye.cn/ip/',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'close'
               }
    r = requests.get(headers=headers, url=url).text
    r = r.replace('\n', '')
    r = r.replace('\t', '')
    r = r.replace('\r', '')
    i = 0
    while True:
        i += 1
        if '查询失败！' in r:
            print_err('查询不到%s精确位置 重试' % ip)
            if i >= 5:
                break
            time.sleep(3)
        elif '纬度' in r:
            loc['jing'] = re.findall('<p>经度：(.*?) \|', r)[0]
            loc['wei'] = re.findall('纬度：(.*?) \|', r)[0]
            print_suc('查询到精确位置: 经度:%s 纬度%s' % (loc['jing'], loc['wei']))
            return loc
        else:
            print_err('未知错误')
            print(r)
            break


def getLoc(ip):
    # print_inf("查询ip归属地中")
    # res = requests.get(url='https://www.ipshudi.com/' + ip + '/', headers=init_headers,proxies=prox)
    # # res.encoding = 'gb2312'
    # print(res.text)
    # r = re.findall('\"ASN归属地\":\"(.*?)\",', res.text)[0]
    # if r == '':
    #     print_err('未查询到ip归属地')
    # else:
    #     print_suc('ip归属地为:' + r)
    url = 'https://whois.pconline.com.cn/ipJson.jsp?ip='
    # print(url+ip)
    f = requests.get(url=url + ip).text
    res = re.findall(',"addr":"(.*?)"', f)
    print_suc(res[0])
    return res[0]


def getMn_acloc(loc):
    url = 'https://api.map.baidu.com/reverse_geocoding/v3/?ak=%s&output=json&coordtype=wgs84ll&location=%s,%s' % (
        'cYW1H9RM0e8QgAHx47Hl4t4Ztav4VRsd', loc['wei'], loc['jing'])
    headers = {'Referer': 'http://www.baidu.com/'}
    r = requests.get(url=url, headers=headers).text
    res = re.findall('"formatted_address":"(.*?)",', r)
    if res is not None:
        print_inf('精确定位可能有偏差')
        print_suc(res[0])
        return res[0]


def getdomain_ip66(ip):
    prox = getproxy()
    i = 0
    while True:
        try:
            res = requests.get('https://site.ip138.com/' + ip, headers=init_headers, proxies=prox).text
            res = res.replace('\n', '')
            res = res.replace('\r', '')
            res = res.replace('\t', '')
            r0 = re.findall('过的域名如下：</span></li>(.*)</ul><a class="btn" href="https://chapangzhan.com/', res)
            if len(r0) != 0:
                r = re.findall('/" target="_blank">(.*?[A-Za-z.])</a></li>', r0[0])
                if r == '':
                    print_err('未查询到域名绑定信息')
                    return r
                else:
                    print_suc('查询到域名绑定信息 共' + str(len(r)) + '条')
                    for it in r:
                        print_inf(it)
                    return r
            else:
                print_err('未查询到域名绑定信息')
                return ''
        except Exception:
            print_err('ERR 重新获取域名信息' + str(i))
            i += 1
            if i >= 5:
                break
            traceback.print_exc()


def getdomain_shodan(ip):
    # get ip from shodan.io
    try:
        apikey = 'QDwpLMQfQpEk3YNJnlQIqyNohJKMXpWv'
        api = shodan.Shodan(apikey)
        seres = api.host(ip)
        print_suc('查询到域名绑定信息 共' + str(len(seres['domains'])) + '条')
        for it in seres['domains']:
            print_inf(it)
        return seres['domains']
    except APIError:
        print_err('shodan未查到相关域名')


def getdomain(ip):  # ip获取域名
    print_inf(blue('从ip66 ip138获取域名绑定信息:'))
    rs = []
    r1 = getdomain_ip66(ip)
    rs = list(r1)
    print_inf(blue('从shodan获取域名绑定信息:'))
    r = getdomain_shodan(ip)
    if r is not None:
        rs += r
    return rs


def getwhoisinf(domain):  # whois获取信息
    # init_headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    # init_headers['Origin'] = 'http://whois.chinaz.com'
    # res = requests.get('http://whois.chinaz.com/' + domain, headers=init_headers)
    # mail = re.findall('', res.text)
    # print(res.text)
    # print_inf('邮箱' + str(mail))
    da = whois.whois(domain)
    inf = {}
    prefix = ''
    if 'CDN' in str(domain).upper():  # 域名关键词过滤
        if details:
            print_err(red('疑似为cdn注册信息 可信度低'))
            prefix += red(' ?CDN? ')
    if 'phone' in da.keys():
        if da['phone'] is None:
            if details:
                print_err(domain + 'whois无电话信息')
        else:
            if isinstance(da['phone'], list):
                for it in da['phone']:
                    if it[0] == 0:
                        if details:
                            print_err(domain + '的电话:' + it + '(疑似非真实电话)' + prefix)
                    else:
                        print_suc(domain + '的电话:' + it + prefix)
                        inf['phone'] = it + prefix
            else:
                it = da['phone']
                if it[0] == 0:
                    if details:
                        print_err(domain + '的电话:' + it + '(疑似非真实电话)' + prefix)
                else:
                    print_suc(domain + '的电话:' + it + prefix)
                    inf['phone'] = it + prefix
    else:
        if details:
            print_err(domain + 'whois无电话信息')
    if 'emails' in da.keys():
        if da['emails'] is None:
            if details:
                print_err(domain + 'whois无邮箱信息')
        else:
            if isinstance(da['emails'], list):
                for it in da['emails']:
                    if 'abuse' in it or 'admin' in it or 'whois' in it or 'Domain' in it or 'privacy' in it or 'REGIS' in str(
                            it).upper():
                        if details:
                            print_err(domain + '的邮箱:' + it + '(疑似非真实邮箱)' + prefix)
                    else:
                        print_suc(domain + '的邮箱:' + it)
                        inf['emails'] = it + prefix
            else:
                itt = da['emails']
                if 'abuse' in itt or 'admin' in itt or 'whois' in itt or 'domain' in itt or 'Domain' in itt or 'privacy' in itt or 'REGIS' in str(
                        itt).upper():
                    if details:
                        print_err(domain + '的邮箱:' + itt + '(疑似非真实邮箱)' + prefix)
                else:
                    print_suc(domain + '的邮箱:' + itt + prefix)
                    inf['emails'] = itt + prefix
    else:
        print_err(domain + 'whois无邮箱信息')
    if 'name' in da.keys():
        if da['name'] is None:
            if details:
                print_err(domain + 'whois无名称信息')
        else:
            if isinstance(da['name'], list):
                for it in da['name']:
                    if 'ADMIN' in str(it).upper() or 'DOMAIN' in str(it).upper() or "PRIVACY" in str(
                            it).upper() or 'REGIS' in str(it).upper():
                        if details:
                            print_err(domain + '的名称:' + it + '(疑似非真实名称)' + prefix)
                    else:
                        print_suc(domain + '的名称:' + it + prefix)
                        inf['name'] = it + prefix
            else:
                it = da['name']
                if 'ADMIN' in str(it).upper() or 'DOMAIN' in str(it).upper() or "PRIVACY" in str(
                        it).upper() or 'REGIS' in str(it).upper():
                    if details:
                        print_err(domain + '的名称:' + it + '(疑似非真实名称)' + prefix)
                else:
                    print_suc(domain + '的名称:' + it + prefix)
                    inf['name'] = it + prefix
    else:
        if details:
            print_err(domain + 'whois无名称信息')
    if debug:
        print(da)
    return inf


# def searchinfo(keyword):
#
def fillter(lis):
    l = []
    if isinstance(lis, list):
        for it in lis:
            if it is None or 'None' == it:  # 去None
                pass
            else:
                re = 0
                for iit in l:
                    if iit == it:
                        re += 1
                if re < 1:  # 去重
                    l.append(it)
    else:
        if lis is None or 'None' == lis:  # 去None
            pass
        else:
            l.append(lis)

    return l


def run(ip):
    ip2inf_res = ip2infres('', '', '', '', '', '', '', '')  # 总结果
    ip2inf_res.ip = ip

    ip2inf_res.loc = getLoc(ip)
    ac = getactLoc(ip)
    if ac is not None:
        acLoc = getMn_acloc(ac)  # 获取精确ip位置
        if acLoc is not None:
            ip2inf_res.loc += acLoc
    domains = getdomain(ip)
    ip2inf_res.domain = domains

    infname = []
    infphone = []
    infmail = []
    noinf = False
    if domains is None:
        noinf = True
    for it in domains:
        try:
            itf = getwhoisinf(it)
            if 'name' in itf.keys():
                infname.append(itf['name'])
            if 'phone' in itf.keys():
                infphone.append(itf['phone'])
            if 'emails' in itf.keys():
                infmail.append(itf['emails'])
        except:
            print_err(it + '无信息')
            traceback.print_exc()
            noinf = True
    if not noinf:
        infname = fillter(infname)
        infphone = fillter(infphone)
        infmail = fillter(infmail)
        print_inf('信息整理:')
        print_inf('  邮箱')
        mail_dtruct = []
        if infmail is not None:
            if not isinstance(infmail, str):
                for it in infmail:
                    if isinstance(it, str):
                        mail_dtruct.append(str(it))
                        print_suc('        ' + str(it))
                    else:
                        for iit in it:
                            print_suc('        ' + str(iit))
                            mail_dtruct.append(str(iit))
            else:
                print_suc('        ' + str(infmail))
        print_inf('  电话')
        if infphone is not None:
            if not isinstance(infphone, str):
                for it in infphone:
                    print_suc('        ' + str(it))
            else:
                print_suc('        ' + str(infphone))
        print_inf('  名称')
        if infname is not None:
            if not isinstance(infname, str):
                for it in infname:
                    print_suc('        ' + str(it))
            else:
                print_suc('        ' + str(infname))
        portr = scan(ip)
        ip2inf_res.services = portr  # 扫描资产
        print_inf('社工库查询中...')
        if len(infmail) >= 1:
            try:
                ip2inf_res.others = sgksearch(mail_dtruct)
            except Exception:
                traceback.print_exc()
        # if infmail is not None:
        #     for it in infmail:
        #         sgksearch(it)

    ip2inf_res.name = infname
    ip2inf_res.tel = infphone
    ip2inf_res.mail = infmail
    return ip2inf_res


def running(ip):
    prefix = ''
    print_inf(ip)
    res1 = run(ip)
    r = res1.to_string()
    if len(r) >= 512:
        prefix = '↑'
    elif len(r) <= 50:
        prefix = '↓↓'
    elif len(r) <= 80:
        prefix = '↓'
    elif len(r) >= 1024:
        prefix = '!'
    while True:  # 保存文件
        try:
            w = open(
                'res' + os.path.sep + datetime.datetime.now().strftime('%Y-%m-%d') + os.path.sep + str(
                    res1.ip) + prefix + '.ipres', 'w')
            w.write(r)
            print_inf('退出脚本 结果保存在' + w.name + os.path.sep + '中')
            w.close()
            break
        except FileNotFoundError:
            if not os.path.exists('res' + os.path.sep + datetime.datetime.now().strftime('%Y-%m-%d')):
                os.makedirs('res' + os.path.sep + datetime.datetime.now().strftime('%Y-%m-%d'))


def run_with_check(t):
    if check_ip(t):
        running(t)
    else:
        resodom = resolve_domain(t)
        if resodom is None:
            print_err('ip地址或域名不正确')
        else:
            running(resodom)


def packagun():  # 最终的运行函数 为了方便线程调用而设计
    if args.v:
        global details
        details = True
    while True:
        if args.f is None and args.i is None:
            print_err('无参数 -h查看')
            exit(1)
        try:
            if args.f is None:
                run_with_check(args.i)  # 查询单个ip
            else:
                try:
                    f = open(args.f).readlines()
                    print_suc('多线程查询中')
                    for it in f:
                        while True:
                            print(threading.active_count())
                            if threading.active_count() <= threadcou:  # 进程数限制
                                t = threading.Thread(name=it.replace('\n', ''), target=run_with_check,
                                                     args=(it.replace('\n', ''),))
                                t.start()
                                break
                            else:
                                time.sleep(1)

                except FileNotFoundError:
                    print_err('输入的文件不存在')

            exit(0)
        except Exception:
            print_err('错误 重试中')
            traceback.print_exc()
        except SystemExit:
            print_inf('中止 退出')
            exit()
        except KeyboardInterrupt:
            print_inf('中止 退出')
            exit()


if __name__ == '__main__':
    # gserv = gevent.spawn(startserv,'127.0.0.1')
    # grun = gevent.spawn(packagun)
    if args.lip is None:
        lip = getlocalip()
        while True:
            ans = input(red('没有输入对外ip 自动获取:%s 是否要应用它?(Y/N) ' % lip))
            if ans.upper() == 'Y':
                args.lip = lip
                break
            elif ans.upper() == 'N':
                print_err('退出')
                exit(0)
            else:
                print_err('未知参数')
    try:
        thrserv = threading.Thread(name='serv', target=startserv, args=(args.lip,))
        thrrun = threading.Thread(name='run', target=packagun)
        thrserv.start()
        thrrun.start()
    except KeyboardInterrupt:
        print_err('中止 退出')

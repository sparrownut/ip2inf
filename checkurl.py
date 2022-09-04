# 222.161.233.0
import re
import threading
import time
import traceback

import requests
from IPy import IP
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import print_suc, print_err, print_inf

threadn_max = 100  # 线程数
debug = False

res = ""
# p = 80
# for i in range(0, 255):
urls = ""

bts = ""
bts_i = 0
urls_i = 0
jsps = ''
jsps_i = 0
asps = ''
asps_i = 0
structs2s = ''
structs2s_i = 0
uprun_i = 0
f = open('test.test', 'r').readlines()
uprun = ""
selenium_is_use = 0

try:
    opt = Options()
    opt.add_argument('--headless')
    cdriver = webdriver.Chrome('chromedriver/chromedriver.exe', options=opt)  # win c driver
    cdriver.implicitly_wait(100)  # wait
    print_inf('selenium启动成功')
except:
    print_err('selenium加载出错')


def geturl(url):
    host = url.replace('https://', '').replace('http://', '')
    global selenium_is_use
    selenium_is_use = 1
    global cdriver
    i = 0
    while host not in cdriver.current_url:  # 防止不匹配
        i += 1
        if i >= 5:
            return ''
        try:
            cdriver.get(url)
            time.sleep(1)
            selenium_is_use = 0
            return cdriver.current_url
        except:
            url = str(url).replace('http://', 'https://')
            cdriver.get(url)
            time.sleep(1)
            selenium_is_use = 0
            return cdriver.current_url


header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://google.com",
}


def trytolink(u):
    global selenium_is_use
    global thr_i
    global res
    global urls
    global bts
    global bts_i
    global urls_i
    global jsps
    global uprun
    global jsps_i
    global asps
    global asps_i
    global structs2s
    global structs2s_i
    global uprun_i
    global threadn
    url = str(u)
    url = url.replace('\n', '')  # refomat
    port = ''
    if len(it.split(':')) >= 2:  # 获取端口
        port = it.split(':')[1]
    else:
        port = '80'
    if 'http://' not in it and 'https://' not in it:  # 识别协议
        if str(port) == '443':
            url = 'https://' + url
        else:
            url = 'http://' + url

    try:

        resb = requests.get(url, headers=header, timeout=10)
        resb.encoding = 'utf-8'
        t = resb.text
        t = t.replace('\n', '')
        t = t.replace('\t', '')
        t = t.replace('\r', '')
        t = t.replace(',', '')
        if '.jsp' in t:
            jsps += "%s\n" % url
            jsps_i += 1
        if '.do"' in t or '.action' in t:
            structs2s += "%s\n" % url
            structs2s_i += 1
        if '.asp' in t:
            asps += "%s\n" % url
            asps_i += 1
        if '登录' in t or '注册' in t or '账号' in t or '密码' in t:
            if '/etc/init.d/bt' in t:
                bts_i += 1
                uprun += "%s\n" % url
            else:
                if '验证码' not in t:
                    uprun += "%s\n" % url
                    uprun_i += 1
        r = re.findall('<title>(.*?)</title>', t)
        while True:
            if r is not None and selenium_is_use == 0:  # 等待selenium释放
                domres = ''
                # if '.cn' in it or '.com' in it:
                #     domres = socket.getaddrinfo(it, None)[0][4][0]
                # else:
                #     domres = host
                # geturlres = geturl(str(url))
                # geturlres = ''
                # res += "%s,%s,%s,%s" % (str(it), r[0], geturlres, domres) + '\n'
                # print_suc("%s,%s,%s,%s" % (str(it), r[0], geturlres, domres))
                # urls += "%s,%s,%s,%s\n" % (str(u), r[0], geturlres, domres)
                # res += "%s,%s,%s" % (url, r[0], geturlres) + '\n'
                # print_suc("%s,%s,%s" % (url, r[0], geturlres))
                # urls += "%s,%s,%s\n" % (url, r[0], geturlres)
                res += "%s,%s" % (str(it), r[0]) + '\n'
                print_suc("%s,%s" % (str(it), r[0]))
                urls += "%s,%s\n" % (str(url), r[0])
                urls_i += 1  # 线程数控制
                threadn -= 1
                thr_i += 1
                return True
            time.sleep(1)
    except:
        print_err('%s(%s/%s)' % (url, thr_i, len(threads)))
        threadn -= 1
        thr_i += 1
        return False


threadn = 0
threads = []
his = ''
for it in f:
    it = it.replace('https://', '')
    it = it.replace('http://', '')  # 过滤为标准地址

    if '/1' in it or '/2' in it:  # 识别是否为CIDR
        if ',' in it:
            for itt in it.split(','):
                try:
                    ips = IP(str(itt))
                    if it not in his:  # 去重
                        for ips_it in ips:  # 迭代
                            threads.append(threading.Thread(target=trytolink, args=(ips_it,)))  # 加入进程
                except:
                    traceback.print_exc()
                    print_err('err-' + itt)
        else:
            try:
                ips = IP(str(it))
                if it not in his:  # 去重
                    for ips_it in ips:  # 迭代
                        threads.append(threading.Thread(target=trytolink, args=(ips_it,)))  # 加入进程
            except:
                print_err('err' + it)
    else:
        if str(it) in his:
            continue  # 去重
        his += it
        threads.append(threading.Thread(target=trytolink, args=(str(it),)))

print_inf('共计%s条任务 线程数为%s' % (len(threads), threadn_max))

thr_i = 0
for thit in threads:
    while True:  # 维持线程数
        if threadn <= threadn_max:
            try:
                thit.start()

            except:
                traceback.print_exc()
            # thit.join()
            if debug:
                print_inf('当前线程数%s/%s' % (threadn, len(threads)))
            threadn += 1

            break

while threadn > 0:  # 等待所有线程完成
    pass

# print(res)
print(urls)
print_suc('导出weburl%s条' % str(urls_i))
print_suc('导出可爆破的登录界面url%s条' % str(uprun_i))
print_suc('导出宝塔面板的url%s条' % str(bts_i))
open('all_web_urls.csv', 'w+').write(urls)
open('login_urls.txt', 'w+').write(uprun)
open('bt_urls.txt', 'w+').write(bts)
print_suc('导出带jsp的url%s条' % str(jsps_i))
open('jsp_urls.txt', 'w+').write(jsps)
print_suc('导出带asp的url%s条' % str(asps_i))
open('asp_urls.txt', 'w+').write(asps)
print_suc('导出带structs2的url%s条' % str(structs2s_i))
open('structs2_urls.txt', 'w+').write(structs2s)

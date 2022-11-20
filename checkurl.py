# coding=utf-8
# 222.161.233.0
import re
import threading
import time
import traceback

import requests
import urllib3
from IPy import IP
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import print_suc, print_err, print_inf

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class check():
    def __init__(self, file_input: str):
        self.f = open(file_input, 'r', encoding='gbk').readlines()

    threadn_max = 10  # 线程数
    debug = False

    threadn = 0
    threads = []
    his = ''
    res = ""
    thr_i = 0
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
    input_file = ''

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

    def geturl(self, url):
        host = url.replace('https://', '').replace('http://', '')
        selenium_is_use = 1
        i = 0
        while host not in self.cdriver.current_url:  # 防止不匹配
            i += 1
            if i >= 5:
                return ''
            try:
                self.cdriver.get(url)
                time.sleep(1)
                selenium_is_use = 0
                return self.cdriver.current_url
            except:
                url = str(url).replace('http://', 'https://')
                self.cdriver.get(url)
                time.sleep(1)
                selenium_is_use = 0
                return self.cdriver.current_url

    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://google.com",
    }

    def trytolink(self, u, isuse=False):
        self.threadn += 1
        ur = str(u)
        ur = ur.replace('\n', '')  # refomat
        port = ''
        if len(ur.split(':')) >= 2:  # 获取端口
            port = ur.split(':')[1]
        else:
            port = '80'
        if 'http://' not in ur and 'https://' not in ur:  # 识别协议
            if str(port) == '443':
                ur = 'https://' + ur
            else:
                ur = 'http://' + ur

        try:
            # print(ur)
            resb = requests.get(ur, headers=self.header, timeout=5, verify=False)
            resb.encoding = 'utf-8'
            t = resb.text
            t = t.replace('\n', '')
            t = t.replace('\t', '')
            t = t.replace('\r', '')
            t = t.replace(',', '')
            if '.jsp' in t:
                self.jsps += "%s\n" % ur
                self.jsps_i += 1
            if '.do"' in t or '.action' in t:
                self.structs2s += "%s\n" % ur
                self.structs2s_i += 1
            if '.asp' in t:
                self.asps += "%s\n" % ur
                self.asps_i += 1
            if '登录' in t or '注册' in t or '账号' in t or '密码' in t:
                if '/etc/init.d/bt' in t:
                    self.bts_i += 1
                    self.uprun += "%s\n" % ur
                else:
                    if '验证码' not in t:
                        self.uprun += "%s\n" % ur
                        self.uprun_i += 1
            r = re.findall('<title>(.*?)</title>', t)
            while True:
                if r is not None and self.selenium_is_use == 0:  # 等待selenium释放
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
                    if not isuse and ('Bad Request'.upper() in str(r[0]).upper() or 'https'.upper() in str(r[0]).upper()):
                        self.trytolink(u=ur.replace('http://','https://'),isuse=True)
                    elif '404' not in r[0] and '403' not in r[0]:
                        self.res += "%s,%s" % (str(ur), r[0]) + '\n'
                        print_suc("%s,%s" % (str(ur), r[0]))
                        self.urls += "%s,%s\n" % (str(ur), r[0])
                        self.urls_i += 1  # 线程数控制
                        self.thr_i += 1
                    else:
                        print_err('%s(%s/%s)' % (ur, self.thr_i, len(self.threads)))
                    break
            self.threadn -= 1
            return True
        except:
            self.threadn -= 1
            if isuse:
                print_err('%s(%s/%s)' % (ur, self.thr_i, len(self.threads)))
                self.thr_i += 1
                return False
            if 'http' in u:
                return self.trytolink(str(u).replace('http', 'https'), True)  # 以https重试
            else:
                return self.trytolink('https://%s' % str(u), True)  # 以https重试

    def run(self):
        for it in self.f:
            # if ',' in it:
            #     it = it.split(',')[0]
            it = it.replace('https://', '')
            it = it.replace('http://', '')  # 过滤为标准地址

            if '/1' in it or '/2' in it:  # 识别是否为CIDR
                if ',' in it:
                    for itt in it.split(','):
                        try:
                            ips = IP(str(itt))
                            if it not in self.his:  # 去重
                                for ips_it in ips:  # 迭代
                                    self.threads.append(threading.Thread(target=self.trytolink, args=(ips_it,)))  # 加入进程
                        except:
                            traceback.print_exc()
                            print_err('err-' + itt)
                else:
                    try:
                        ips = IP(str(it))
                        if it not in self.his:  # 去重
                            for ips_it in ips:  # 迭代
                                self.threads.append(threading.Thread(target=self.trytolink, args=(ips_it,)))  # 加入进程
                    except:
                        print_err('err' + it)
            else:
                if str(it) in self.his:
                    continue  # 去重
                self.his += it
                self.threads.append(threading.Thread(target=self.trytolink, args=(str(it),)))

        print_inf('共计%s条任务 线程数为%s' % (len(self.threads), self.threadn_max))
        for thit in self.threads:
            while True:  # 维持线程数
                if self.threadn <= self.threadn_max:
                    try:
                        thit.start()

                    except:
                        traceback.print_exc()
                    # thit.join()
                    if self.debug:
                        print_inf('当前线程数%s/%s' % (self.threadn, len(self.threads)))

                    break

        while self.threadn > 0:  # 等待所有线程完成
            pass

        # print(res)
        print(self.urls)
        print_suc('导出weburl%s条' % str(self.urls_i))
        print_suc('导出可爆破的登录界面url%s条' % str(self.uprun_i))
        print_suc('导出宝塔面板的url%s条' % str(self.bts_i))
        open('all_web_urls.csv', 'w+', encoding='utf-8').write(self.urls)
        open('login_urls.txt', 'w+').write(self.uprun)
        open('bt_urls.txt', 'w+').write(self.bts)
        print_suc('导出带jsp的url%s条' % str(self.jsps_i))
        open('jsp_urls.txt', 'w+').write(self.jsps)
        print_suc('导出带asp的url%s条' % str(self.asps_i))
        open('asp_urls.txt', 'w+').write(self.asps)
        print_suc('导出带structs2的url%s条' % str(self.structs2s_i))
        open('structs2_urls.txt', 'w+').write(self.structs2s)
        return self.res


if __name__ == '__main__':
    check('test.test').run()

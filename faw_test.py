# 222.161.233.0
import re
import time

import requests

from utils import print_suc, print_err

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://google.com",
}
res = ""
# p = 80
# for i in range(0, 255):
urls = ""
bts = ""
bts_i = 0
urls_i = 0
uprun_i = 0
f = open('test.test', 'r').readlines()
uprun = ""
# for it in f:
a = 219
for b in range(0, 255):
    time.sleep(0.1)
    it = '111.26.%s.%s:80' % (str(a), str(b))
    if str(it) in urls:
        continue  # 去重
    it = it.replace('\n', '')
    host = it.split(':')[0]
    p = it.split(':')[1]
    u = ''
    if str(p) == '443':
        u = 'https://' + str(it)
    else:
        u = 'http://' + str(it)
    # if portscan(host, p):
    #     r = []
    try:
        t = requests.get(u, headers=header, timeout=0.5).text
        t = t.replace('\n', '')
        t = t.replace('\t', '')
        t = t.replace('\r', '')
        t = t.replace(',', '')

        if '登录' in t or '注册' in t or '账号' in t or '密码' in t:
            if '/etc/init.d/bt' in t:
                bts_i += 1
                uprun += "%s\n" % u
            else:
                if '验证码' not in t:
                    uprun += "%s\n" % u
                    uprun_i += 1
        if 'CDN' in t:
            continue  # 去CDN
        r = re.findall('<title>(.*?)</title>', t)
        if r is not None:
            res += "%s,%s" % (str(it), r[0]) + '\n'
            print_suc("%s-%s" % (str(it), r[0]))
            urls += "%s\n" % (str(u))
            urls_i += 1
    except:
        print_err("%s" % (str(it)))
        # res += "%s:%s"%(u,str(p)) + '\n'
        pass
    # else:
    #     print_inf("%s:%s not" % (u, str(p)))

print(res)
print(urls)
print_suc('导出weburl%s条' % str(urls_i))
print_suc('导出可爆破的登录界面url%s条' % str(uprun_i))
print_suc('导出宝塔面板的url%s条' % str(bts_i))
open('all_web_urls.txt', 'w+').write(urls)
open('login_urls.txt', 'w+').write(uprun)
open('bt_urls.txt', 'w+').write(bts)
open('all_web_urls_withdescript.txt', 'w+').write(str(res))

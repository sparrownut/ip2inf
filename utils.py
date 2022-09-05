import datetime
import difflib
import random
import re
import socket
import requests
import urllib3.exceptions

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def green(s):
    return '\033[32m' + s + '\033[0m'


def red(s):
    return '\033[31m' + s + '\033[0m'


def blue(s):
    return '\033[36m' + s + '\033[0m'


def yellow(s):
    return '\033[33m' + s + '\033[0m'


def print_suc(s):
    print(blue(str(datetime.datetime.now())) + green(" [+] ") + str(s))


def print_err(s):
    print(blue(str(datetime.datetime.now())) + red(" [-] ") + str(s))


def getproxy(checkurl='https://www.baidu.com',v = False):
    reet = {}
    r = requests.get('https://free-proxy-list.com/', headers=init_headers).text
    ree = re.findall('alt="(.*)" title="', r)  # 分离代理信息
    if v:
        print_inf('连接代理池中')
    st = True
    while st:
        try:
            reet['http'] = ree[random.randint(0, 9)]
            if '200' not in str(
                    requests.get(url=checkurl, proxies=reet, headers=init_headers, timeout=5,
                                 verify=False).status_code):
                st = False
            break

        except Exception:
            # print(reet)
            if v:
                print_err('更换')
    if v:
        print_suc('连接成功')
    return reet


def print_inf(s):
    print(blue(str(datetime.datetime.now())) + yellow(" [!] ") + str(s))


def check_ip(ipAddr):
    compile_ip = re.compile(
        '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if compile_ip.match(ipAddr):
        return True
    else:
        return False


init_headers = {'Sec-Ch-Ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': 'Sec-Ch-Ua-Platform',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/103.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                          '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                }


def generate_random_str(randomlength=8):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


def resolve_domain(domain):  # 解析域名
    hostip = ''

    try:
        hostip = socket.gethostbyname(domain)
        print(hostip)
    except socket.error as e:
        return None
    return hostip


def getlocalip():
    try:
        url = 'https://whois.pconline.com.cn/ipJson.jsp'
        r = requests.get(url, headers=init_headers).text
        r = r.replace('\n', '')
        r = r.replace('\r', '')
        r = r.replace('\t', '')
        r = r.replace(' ', '')
        rre = re.findall('"ip":"(.*?)","pro', r)
        if rre is not None:
            r = rre[0]
        else:
            print_err('获取本地ip错误 请手动输入本地对外ip')
            exit(0)
        return str(r)
    except Exception:
        print_err('获取本地ip错误 请手动输入本地对外ip')
        exit(0)


# print(getlocalip())
def fixrespo(text):
    text = text.replace(' ', '')
    text = text.replace('\n', '')
    text = text.replace('\t', '')
    text = text.replace('\r', '')
    return text
def str_sim(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()  # 计算文本相似度
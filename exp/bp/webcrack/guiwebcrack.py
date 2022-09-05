from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opt = Options()
opt.add_argument('--headless')

cdriver = webdriver.Chrome('../chromedriver/chromedriver.exe',op)
cdriver.maximize_window()

def sendfrom(url, pwd, una):
    cdriver.implicitly_wait(100)
    cdriver.get(url)
    resp1 = cdriver.page_source
    print(resp1)

# def bf(url):
#

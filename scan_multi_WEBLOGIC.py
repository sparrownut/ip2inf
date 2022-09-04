import os

f = open('all_web_url.txt', 'r')
for it in f.readlines():
    print(str(it))
    s = os.system('python3 ws.py -t %s' % str(it))

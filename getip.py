import os
import re

from utils import print_suc, print_err

inp = open('test.test', 'r').readlines()
domres = ''
for it in inp:
    try:
        it = it.replace('/', '')
        it = it.replace('https', '')
        it = it.replace('http', '')
        host = it
        if ':' in it:
            host = it.split(':')[0]
            port = it.split(':')[1]
        it = it.replace(':', '')
        # print(str(os.system('ping %s' % it)))
        domainres = re.findall('\[(.*?)\]', os.popen('ping -n 1 %s' % it, 'r').read().replace('\n', ''))[0]
        # domainres = re.findall('\[(.*?)\]', )[0]
        # print_suc(domainres)
        domres += '%s,%s\n' % (domainres, it)
        print_suc('%s,%s\n' % (domainres, it))
    except:
        # traceback.print_exc()
        print_err('%s' % it)
out = open('domain2ip.csv', 'w+')
out.write(domres)

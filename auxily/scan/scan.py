main = open('main.list', 'r').readlines()
exp = open('exp.list', 'r').readlines()
res = ''


def getc(ip):
    return "%s.%s.%s" % (str(ip).split('.')[0], str(ip).split('.')[1], str(ip).split('.')[2])


for it in main:
    for itt in exp:
        try:
            if ':' in it:
                mit = it.split(':')[0]  # main iplist
            else:
                mit = it
            if ':' in itt:
                eit = itt.split(':')[0]  # exploit iplist
            else:
                eit = itt
            if mit is not None and eit is not None:
                mc = getc(mit)
                ec = getc(eit)
                if mc == ec:  # 如果处于同一网段
                    if eit not in res:
                        print("%s (目标资产) - %s (有可利用漏洞的资产)\n" % (mit, eit))
                        res += "%s:%s\n" % (eit, itt.split(':')[1])
        except:
            pass
open('output.txt', 'w+').write(res)

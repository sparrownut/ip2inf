import os
import traceback

import nmap

from utils import print_inf, print_suc, print_err


def tempscanport(ip):  # 扫描主机资产

    print_inf('扫描' + ip + '资产...')
    tp_res = ''
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        nm = nmap.PortScanner(('nmap', path + os.path.sep + 'Nmap' + os.path.sep + 'nmap.exe'))
        nm.scan(ip)
        if 'tcp' in nm[ip].keys():
            dic = nm[ip]['tcp']
            data = {}
            for it in dic.items():
                # print(str(it[1]))
                product = it[1]['product']
                if 0 == len(str(product)):
                    product = '未知服务'
                ver = it[1]['version']
                if len(str(ver)) == 0:
                    ver = '未知版本'
                print_suc('--' + str(it[0]) + ' ' + product + ' ' + ver + ' ' + it[1]['cpe'])
                data['product'] = it[1]['product']
                data['version'] = it[1]['version']
                data['cpe'] = it[1]['cpe']
                tp_res += str(it[0]) + ';' + product + ';' + ver + ';' + it[1]['cpe'] + '\n'
        else:
            print_err('扫描不到主机资产 疑似不在线')
    except KeyError:
        try:
            print_err('ICMP未开放 切换扫描模式')
            path = os.path.dirname(os.path.abspath(__file__))

            nm = nmap.PortScanner(('nmap', path + os.path.sep + 'Nmap' + os.path.sep + 'nmap.exe'))
            nm.scan(ip, '-Pn')
            if 'tcp' in nm[ip].keys():
                dic = nm[ip]['tcp']
                data = {}
                for it in dic.items():
                    # print(str(it[1]))
                    product = it[1]['product']
                    if 0 == len(str(product)):
                        product = '未知服务'
                    ver = it[1]['version']
                    if len(str(ver)) == 0:
                        ver = '未知版本'
                    print_suc('--' + str(it[0]) + ' ' + product + ' ' + ver + ' ' + it[1]['cpe'])
                    data['product'] = it[1]['product']
                    tp_res += str(it[0]) + ';' + product + ';' + ver + ';' + it[1]['cpe'] + '\n'
                    data['version'] = it[1]['version']
                    data['cpe'] = it[1]['cpe']
            else:
                print_err('扫描不到主机资产 不在线')
        except KeyError:
            print_err('疑似为住宅主机或没有开启任何服务')
    return tp_res


def scan(ip):  # 协程扫
    try:
        # g1 = gevent.spawn(tempscanport, ip)
        # g1.join()
        return tempscanport(ip)
    except Exception:
        print_inf('err')
        traceback.print_exc()

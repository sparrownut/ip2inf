import socket
import threading

from utils import print_inf

f = open('portscan.input', 'r')
threads = []


def portscan(host, port):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(2)  # 设置超时时间
    try:
        sk.connect((host, port))
        sk.close()
        return True
    except Exception:
        sk.close()
        return False


for host in f.readlines():
    for port in range(1, 65536):
        threads.append(threading.Thread(target=portscan, args=(host, port,)))
print_inf('共%s任务' % len(threads))

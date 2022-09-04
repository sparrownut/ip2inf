import socket

from utils import print_suc


class sshScan:
    def conn_port(self, host, port):
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(2)  # 设置超时时间
        try:
            sk.connect((host, port))
            recv = sk.recv(1024)
            sk.close()
            if b"SSH" in recv:
                return True
            else:
                return False
        except Exception:
            sk.close()
            return False

    def ssh_scan(self, host, port):
        res = self.conn_port(host, port)
        if res:
            print_suc(host + "在" + str(port) + '端口上的SSH服务开启')
            return True
        return False

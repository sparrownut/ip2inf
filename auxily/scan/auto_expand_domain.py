# coding=utf-8
import base64
import json

import requests

# import checkurl
from utils import print_suc, print_inf


def get_root_domain(domain: str):
    r = domain.split('.')
    if r is not None:
        if len(r) > 2:
            return domain.replace(r[0] + '.', '')
        else:
            return domain


def get_from_fofa(domain: str):
    input = base64.b64encode(bytes(('domain=' + domain).encode())).decode()
    api = 'https://fofa.info/api/v1/search/all?email=om2bg0tjsptuh7weetboc2t7vvzk@open_wechat&key' \
          '=fff73dae777ddbcf971bb5e85f2ae3aa&size=10000&qbase64=' + input
    # print(api)
    text = requests.get(url=api).text
    res2 = json.loads(text)['results']
    res = []
    for it in res2:
        res.append(it)
    return res


def url2domain(url: str):
    domain = ''
    url = url.replace('http', '')
    url = url.replace('https', '')
    url = url.replace('://', '')
    url = url.replace(' ', '')
    url = url.replace('\t', '')
    url = url.replace('\n', '')
    if ':' in url:
        port_split = url.split(':')
        domain = port_split[0]
    elif '/' in url:
        url_split = url.split('/')
        domain = url_split[0]
    else:
        domain = url
    return domain


if __name__ == '__main__':  # 从文件夹读取url列表并批量扩张资产再验证
    input_url = open('input_dir/url.input', 'r', errors=None).readlines()
    open('output_dir/output.txt', 'w', errors=None).write('')  # 清除文件内容
    res_output = open('output_dir/output.txt', 'a', errors=None)
    print_inf('扩张资产中')
    reslist = []
    for it in input_url:
        it = it.replace('\n', '')
        domain = url2domain(it)  # 从url获取域名
        root_domain = get_root_domain(domain)
        print_inf(root_domain)
        domain_expand_list = get_from_fofa(root_domain)  # 从fofa调用api增加资产
        list_len = len(domain_expand_list)
        print_suc('从fofa获取到%s域名的%s资产' % (it, list_len))
        for itt in domain_expand_list:
            # print(itt[0])
            res_output.write(itt[0] + '\n')
            reslist.append(itt)
    print_suc('扩张完毕')
    # print_inf('检查可用性中')
    # output_res_list = []
    #
    # for it in reslist:
    #     for itt in checkurl.check(it).run():
    #         output_res_list.append(itt)
    # for it in output_res_list:
    #     res_output.write(it + '\n')

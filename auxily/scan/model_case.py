# coding=utf8
import traceback

import requests

from utils import print_suc, print_inf

if __name__ == '__main__':
    hashlist = []
    r = open('input_dir/列表.txt', 'r', encoding='utf8', errors=None)
    # a = open('input_dir/hashlist.txt','ar')
    for it in r.readlines():
        try:
            it = it.replace('\n', '')
            rtex = requests.get(it).text
            hash_v = hash(rtex)
            if '番号' in rtex:
                print_suc('番号cms:%s' % it)
            if hash_v not in hashlist:
                print_suc('新hash: hash(%s)=%s' % (it, hash_v))
                w = open('output_dir/%s.txt' % hash_v, 'w')
                w.write(it + '\n')
                w.close()
                hashlist.append(hash_v)
            else:
                print_inf('%s 已经存在此hash' % it)
                w = open('output_dir/%s.txt' % hash_v, 'a')
                w.write(it + '\n')
                w.close()
        except Exception:
            traceback.print_exc()
# if __name__ == '__main__':
#     g = os.walk('output_dir')
#     for path, dir_list, file_list in g:
#         for file_name in file_list:
#             r = open(os.path.join(path, file_name)).readlines()[0]
#             print(r)

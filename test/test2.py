import hashlib
from itertools import permutations

from utils import print_suc, print_inf


#

# # i = 0
# # for it in input_.readlines():
# #     for itt in input2.readlines():
# #         print(it.split(',')[1]+' '+itt.split(',')[0])
# #         if it.split(',')[1] == itt.split(',')[0]:
# #             output.write(it+itt)
# #             i += 1
# #             print_suc(str(i))
def md5(string: str):
    hh = hashlib.md5()
    hh.update(string.encode())
    return hh.hexdigest()


if __name__ == '__main__':
    # print_inf('生成规则中')
    # arr = ['it','s1','s2'] # 所有元素
    # p_arr_1 = list(permutations(arr,1)) # 排列组合
    # p_arr_2 = list(permutations(arr, 2))  # 排列组合
    # p_arr_3 = list(permutations(arr, 3))  # 排列组合
    s1 = 'MGFssntwrP'
    s2 = 'tYTFSkHEnKrr'
    pwd_md5 = 'ac328b00fc89a125623fc03eae4794c0'
    p = 'qq112233'
    read = open('../exp/bp/crunch.txt', 'r', encoding='utf8')
    r = read.readlines()
    # print_inf(len(r) * len(r))
    for it in open('../exp/bp/crunch.txt').readlines():
        for code_it in open('eval.md5').readlines():
            it = it.replace('\n','')
            code_it = code_it.replace('\n', '')
            it = md5(it)
            code = eval(code_it)
            # print(code)
            md5_encode = md5(code)
            # print_inf(md5_encode)
            if md5_encode == pwd_md5:
                print_suc(code_it)
                print_suc(md5_encode)
                print_suc(code)
                exit(0)
    #
# def decode_md5(string, salt1: bytes, salt2: bytes):
#     read = open('../exp/bp/rockyou.txt', 'r', errors='ignore', encoding='utf8').readlines()
#     # i = 0
#     for it in read:
#         # i += 1
#         # print(i)
#         # it = it.replace('\n', '')
#         # # print(salt1+it.encode()+salt2)
#         # hh.update(it.encode() + salt2 + salt1)  # 解密函数
#         # print(hh.hexdigest())
#         if (hh.hexdigest()) == string:
#             print_suc('%s,%s' % (string, it))
#             return '%s,%s' % (string, it)
#     return string
#
#
# read = open('t_manage.csv', 'r', encoding='utf8')
# res = ''
# i = 0
# c = 0
# for it in read.readlines():
#     c += 1
#     print(c)
#     try:
#         # i += 1
#         # print(i)
#         salt1 = it.split(',')[4]
#         salt2 = it.split(',')[8]
#         md5_encoded = it.split(',')[13]
#         r = decode_md5(salt1=bytes(salt1.encode()), salt2=bytes(salt2.encode()), string=md5_encoded)
#         if ',' in r:
#             print_suc(r + ':' + str(i))
#             res += r + '\n'
#     except:
#         traceback.print_exc()
# print(res)

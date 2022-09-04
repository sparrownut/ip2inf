from itertools import product

l = ['ccut', '123', '1234', '12345', '1', '2', 'admin', 'password']
list1 = list(product(l))
res = ''
for it in list1:
    for iit in it:
        res += str(iit)
    res += '\n'
list2 = list(product(l, l))
for it in list2:
    for iit in it:
        res += str(iit)
    res += '\n'
list3 = list(product(l, l, l))
for it in list3:
    for iit in it:
        res += str(iit)
    res += '\n'
open('pwd_output.txt', 'w+').write(res)

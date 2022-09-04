x = open('output_dic.txt', 'w+')
b = ''
for a in 'abcdefghijklmnopqrstuvwxyz':
    for b in 'abcdefghijklmnopqrstuvwxyz':
        for c in 'abcdefghijklmnopqrstuvwxyz':
            b += "%s%s%s" % (a, b, c)
            print("%s%s%s" % (a, b, c))
x.write(b)

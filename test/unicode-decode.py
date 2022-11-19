if __name__ == '__main__':
    input_name = 'rabbos_zw_user_address.csv'
    output_name = 'rabbos_zw_user_address_dec.csv'
    read = open(input_name, 'r', encoding='gb18030').readlines()
    open(output_name, 'w+', encoding='utf-8')
    open(output_name, 'w+', encoding='utf8')
    output = open(output_name, 'a', encoding='gb18030',errors=None)

    for it in read:
        try:
            output.write(it.encode().decode('unicode_escape'))
        except:
            pass
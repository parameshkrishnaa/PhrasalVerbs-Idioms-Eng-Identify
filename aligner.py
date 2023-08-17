line_1 = "20 bảng Anh là một món tiền lớn đối_với một người nghèo ."
line_2 = "NULL ({ 4 5 }) £ ({ 2 3 }) 20 ({ 1 }) means ({ 6 7 8 9 }) a_lot ({ }) to ({ }) a ({ 10 }) poor ({ 11 12 }) person ({ }) . ({ 13 })"
token_list_1 = line_1.split()
token_list_2 = line_2.split()
aligned = ''
flag = True
correspond_token_list = []
for token in token_list_2:
    if True == flag:
        if '({' == token:
            flag = False
            aligned += '('
            correspond_token_list = []
        else:
            aligned += token + ' '
    else:
        if '})' == token:
            flag = True
            aligned += ','.join(correspond_token_list) + ') '
        else:
            correspond_token_list.append(token_list_1[int(token)-1])
print (aligned)
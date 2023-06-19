for i in range(3,15):
    str_1 = 'BDS-L3-'
    if i < 10:
        i = str(i)
        print(str_1+'0'+i)
    else:
        i = str(i)
        print(str_1+i)
    
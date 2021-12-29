def marsExploration(s):
    valid_chars = 'SOS'
    res = 0
    for i in range(0,len(s[:-2]),3):
#        print(s[i],s[i+1],s[i+2])
        a= s[i] != "S" 
        b= s[i+1] != "O" 
        c= s[i+2] != 'S'
        d = (a+ b + c)
        res += d
    return res

# marsExploration('SOSSOT')
print(marsExploration('SOSOOSOSOSOSOSSOSOSOSOSOSOS'))

# def marsExploration(s):
#     valid_chars = 'SOS'
#     res = 0
#     amount = len(s)//3
#     for i in s:
        
#     return res

# print(marsExploration('SOSOOSOSOSOSOSSOSOSOSOSOSOS'))
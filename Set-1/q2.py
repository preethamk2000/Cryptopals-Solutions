a = "1c0111001f010100061a024b53535009181c"
b = "686974207468652062756c6c277320657965"

a = bytes.fromhex(a)
b = bytes.fromhex(b)

c = ""
c_hex = ""

for i in range(len(a)):
    c += chr(a[i]^b[i])
    c_hex += "{0:0{1}x}".format(a[i]^b[i],2)
    #print(i,c,c_hex)

print(c_hex)
print(c)

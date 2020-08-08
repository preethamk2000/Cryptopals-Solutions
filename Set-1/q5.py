string = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = "ICE"

byteString = string.encode('ascii')
byteKey = key.encode('ascii')

count = 0
ciphertext = ""

for i in byteString:
    ciphertext = ciphertext + chr( i ^ byteKey[count%len(key)] ) 
    count = count + 1

print(ciphertext.encode('ascii').hex())
# print(ciphertext)
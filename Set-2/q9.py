from string import printable

# KEY POINT LEARNT: WHEN APPENDING HEX STRINGS LIKE \X01 ETC. OPERATE IN BYTES AND NOT IN STRINGS
# BECAUSE IN STRINGS IT GETS COMPLICATED DUE TO THE FACT THAT UNNECESSARY '\' CHARACTERS GET APPENDED TOGETHER
# IE '\X01' BECOMES '\\X01' AND ITS SO CALLED HEX-I-NESS GETS LOST :P

# Remove unnecessary elements from printable characters
printable_refined = printable[0:len(printable)-5]

# Accepts a string and returns padded plaintext as bytearray
def pkcs7_padding(plaintext,blocksize=8):
    if type(plaintext)==str:
	# Change to bytes here if needed
        padded_text = plaintext.encode('ascii')
    elif type(plaintext)==bytes:
        padded_text = plaintext
    if len(plaintext)%blocksize != 0:
        padding_length = blocksize-len(plaintext)%blocksize
        padding_string = "{:02x}".format(padding_length)
        for i in range(padding_length):
            padded_text += bytes.fromhex(padding_string)
    return padded_text

def pkcs7_padding_remove(padded_text,blocksize=8):
    # Since it is in bytes, the individual elements are already in INT
    lastchr_int = padded_text[::-1][0]
    # Here Im just checking if the last hex is a printable character and if it is then it must be a block with a multiple of keysize since even with keysize of 32 bytes all the characters do not have meaning when printable
    if(printable_refined.find( chr(lastchr_int) )!=-1):
        return padded_text
    else:
        # padding_length = int.from_bytes(padded_text[::-1][0].encode(),"little")
        # plaintext = padded_text[0:len(padded_text)-padding_length]
        # OR FOR SIMPLER SHIT
        plaintext = padded_text[0: -lastchr_int ]
        return plaintext

if __name__=="__main__":
    plaintext = "YELLOW SUBMARINE"
    # plaintext = "012345678901234567890123"
    # plaintext = "YELLOW SUBMARINEYELLOW SUBMARINEYELLOW SU"
    blocksize = 20

    padded_text = pkcs7_padding(plaintext,blocksize)
    print("\nPlaintext ->" + plaintext + "<- padded to blocksize of " + str(blocksize) + " is :")
    print(padded_text)

    print("\n----------Removing padding----------------")
    original_plaintext = pkcs7_padding_remove(padded_text,blocksize)
    print("Original text: ",original_plaintext)

    print(len(padded_text))

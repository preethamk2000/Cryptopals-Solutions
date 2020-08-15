from string import printable
import io

printable_refined = printable[0:len(printable)-5]

def pkcs7_padding(plaintext,blocksize=8):
    padded_text = "" + plaintext
    padding_length = blocksize-len(plaintext)%blocksize
    padding_string = "\\x{:02x}".format(padding_length)
    for i in range(padding_length):
        padded_text += padding_string
    return padded_text

def pkcs7_padding_remove(padded_text,blocksize=8):
    # FUCKING PYTHON ADDS ANOTHER '\' CHARACTER EVEN FOR \X?? TYPE HEX DIGITS
    # lastchr = padded_text[::-1][0]
    # So instead get the last two hex digits and use them to un pad 
    lastchr = padded_text[len(padded_text)-2:len(padded_text)]
    lastchr_int = int(lastchr,16)
    # Here Im just checking if the last hex is a printable character and if it is then it must be a block with a multiple of keysize
    if(printable_refined.find( chr(lastchr_int) )!=-1):
        return padded_text
    else:
        # padding_length = int.from_bytes(padded_text[::-1][0].encode(),"little")
        # plaintext = padded_text[0:len(padded_text)-padding_length]
        # OR FOR SIMPLER SHIT
        # This 4 is added
        plaintext = padded_text[0: -4*lastchr_int ]
        return plaintext

if __name__=="__main__":
    # plaintext = "YELLOW SUBMARINE"
    plaintext = "012345678901234567890123"
    # plaintext = "YELLOW SUBMARINEYELLOW SUBMA"
    blocksize = 32
    if len(plaintext)%blocksize != 0:
        padded_text = pkcs7_padding(plaintext,blocksize)
    else:
        padded_text = plaintext
    print("Plaintext ->" + plaintext + "<- padded to " + str(blocksize) + " blocks is :" + padded_text + "--------END")

    # padded_text = "12345678"

    print("----------Removing padding----------------")
    original_plaintext = pkcs7_padding_remove(padded_text,blocksize)
    print("Original text: " + original_plaintext)
def pkcs7_padding(plaintext,blocksize=8):
    padded_text = "" + plaintext
    padding_length = blocksize-len(plaintext)%blocksize
    padding_string = "\\x{:02x}".format(padding_length)
    for i in range(padding_length):
        padded_text += padding_string
    return padded_text


if __name__=="__main__":
    # plaintext = "YELLOW SUBMARINE"
    plaintext = "YELLOW SUBMARINEYELLOW SUBMARINEYELLOW S"
    blocksize = 20
    if len(plaintext)%blocksize != 0:
        padded_text = pkcs7_padding(plaintext,blocksize)
    else:
        padded_text = plaintext
    print("Plaintext ->" + plaintext + "<- padded to " + str(blocksize) + " blocks is :" + padded_text)
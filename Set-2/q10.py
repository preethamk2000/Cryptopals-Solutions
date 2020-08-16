from q9 import pkcs7_padding,pkcs7_padding_remove
from q7 import AES_ECB
import base64

class AES_CBC:

    def __init__(self,key,IV):
        self.ecb_scheme = AES_ECB(key)
        self.IV = IV
        self.key = key
    
    def encrypt(self,plaintext_unpadded):
        blocksize = len(self.key)
        plaintext = pkcs7_padding(plaintext_unpadded,blocksize)
        no_of_blocks = int(len(plaintext)/blocksize)
        prev_cipherblock = self.IV
        ciphertext = "".encode('ascii')
        for i in range(no_of_blocks):
            plaintext_block = plaintext[blocksize*i:blocksize*(i+1)]
            intermediate_cipherblock = "".encode('ascii')
            for j in range(blocksize):
                intermediate_cipherblock += bytes( [ plaintext_block[j]^prev_cipherblock[j] ] )
            cipherblock = self.ecb_scheme.encrypt(intermediate_cipherblock)
            prev_cipherblock = cipherblock
            ciphertext += cipherblock
        return ciphertext

    def decrypt(self,ciphertext):
        blocksize = len(self.key)
        no_of_blocks = int(len(ciphertext)/blocksize)
        prev = self.IV
        plaintext = "".encode("ascii")
        for i in range(no_of_blocks):
            ciphertext_block = ciphertext[blocksize*i:blocksize*(i+1)]
            # intermediate_plaintext_block = "".encode('ascii')
            intermediate_plaintext_block = self.ecb_scheme.decrypt(ciphertext_block)
            plaintext_block = "".encode('ascii')
            for j in range(blocksize):
                # intermediate_plaintext_block += bytes( [ ciphertext_block[j]^key[j] ] )
                plaintext_block += bytes( [ intermediate_plaintext_block[j]^prev[j] ] )
            prev = ciphertext_block
            plaintext += plaintext_block
        plaintext = pkcs7_padding_remove(plaintext,blocksize)
        return plaintext


if __name__=="__main__":
    plaintext = "Hello there, fellow netizen! I hope you're doing ok."
    key = "YELLOW SUBMARINE".encode('ascii')
    IV = bytes.fromhex("00"*16)
    cbc_scheme = AES_CBC(key,IV)

    ciphertext = cbc_scheme.encrypt(plaintext)
    print("------------Encrypted Text--------------")
    print(ciphertext,len(ciphertext))

    print("--------Decrypted Text-----------")
    plaintext_decrypted = cbc_scheme.decrypt(ciphertext)
    print(plaintext_decrypted)


    print("\n---------------Decrypted File------------------")
    with open('10.txt','rb') as file:
        ciphertext = base64.b64decode(file.read())
        unpadded_plaintext = cbc_scheme.decrypt(ciphertext)
    print(unpadded_plaintext.decode())
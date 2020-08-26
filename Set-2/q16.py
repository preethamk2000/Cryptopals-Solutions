from q10 import AES_CBC
from os import urandom
from q14 import prepend_length_guesser

class AES128_CBC_Oracle:
    
    def __init__(self):
        key = urandom(16)
        IV = urandom(16)
        self.cbc_scheme = AES_CBC(key,IV)

    def encrypt(self,plaintext):
        if type(plaintext) == str:
            plaintext = plaintext.encode()
        prepend = "comment1=cooking%20MCs;userdata="
        append = ";comment2=%20like%20a%20pound%20of%20bacon"
        plaintext = prepend.encode('ascii') + plaintext + append.encode('ascii')
        plaintext = plaintext.replace(b"=",b"'='").replace(b";",b"';'")
        ciphertext = self.cbc_scheme.encrypt(plaintext)
        return ciphertext

    def decrypt(self,ciphertext):
        plaintext = self.cbc_scheme.decrypt(ciphertext)
        plaintext = plaintext.replace(b"'='",b"=").replace(b"';'",b";")
        return plaintext

# Function where the bitflipping takes place
def attack(oracle,prepend_bytes_to_blocksize,blocksize=16):
    plaintext = "A"*(prepend_bytes_to_blocksize+blocksize)
    ciphertext = oracle.encrypt(plaintext)
    required_string = ";admin=True;".encode('ascii')
    for i in range(len(required_string)):
        # Need to xor the actual plaintext with resultant plaintext
        xor_char = "A".encode()[0]^required_string[i]
        # This is done in the block before our input text(here 3rd), so that while decrypting it changes the next block
        ciphertext = ciphertext[0:32+i] + bytes([ ciphertext[32+i]^xor_char ]) + ciphertext[32+i+1:]
    return ciphertext 

def check_admin(plaintext):
    keys = plaintext.split(b";")
    isAdmin = False
    for i in keys:
        key = i.split(b"=")
        if key[0] == b"admin":
            isAdmin = key[1]
    return isAdmin 


if __name__=="__main__":

    oracle = AES128_CBC_Oracle()

    _,_,bytes_to_blocksize = prepend_length_guesser(oracle)
    edited_ciphertext = attack(oracle,bytes_to_blocksize,16)
    plaintext = oracle.decrypt(edited_ciphertext)

    print("-------------Tampered Ciphertext Decrypted---------------")
    print(plaintext)
    isAdmin = check_admin(plaintext)
    if isAdmin:
        print("Admin message is true!")
    else:
        print("Not an admin message!")
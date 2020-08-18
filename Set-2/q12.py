import base64
from math import ceil
from q10 import AES_CBC,AES_ECB

class AES128_Encryption_Oracle:
    
    def __init__(self):
        # self.key = urandom(keysize)
        self.key = b"\xdf\x00\x85\x91\\\x9dJ\xd1\xda\x984\x05m\xd76\xd2"
    
    def preprocess(self,plaintext):
        append = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
        append = base64.b64decode(append)
        plaintext = plaintext + append
        return plaintext
    
    def encrypt(self,plaintext):
        if type(plaintext)==str:
            plaintext = plaintext.encode('ascii')
        plaintext = self.preprocess(plaintext)

        enc_scheme = AES_ECB(self.key)
        
        ciphertext = enc_scheme.encrypt(plaintext)
        return ciphertext

# Gets the last byte of the block (or next byte of secret string) (block by block) by comparing it with all possible values of the last character's encryption by querying the oracle
def last_byte_crack(plaintext,ciphertext,oracle,iter):
    possible_vals = {}

    if type(plaintext)==str:
        plaintext = plaintext.encode('ascii')

    for i in range(128):
        # We encrypt and find values for all characters, if needed change 128 to 256 max
        # The value of iteration is needed here, since as we go further into getting the secret text values
        # we go to next blocks and so keysize*iteration no. is needed 
        val = oracle.encrypt(plaintext+bytes([i]))
        possible_vals[val[16*iter:16*(iter+1)]] = plaintext+bytes([i])
    
    # Since all values are there in the dict, we get the reverse value i.e,
    # the text which gives the corresponding encryption which is there in the ciphertext
    answer = possible_vals[ciphertext[16*iter:16*(iter+1)]]

    # print(answer.replace(plaintext.decode(),""))
    # print(answer)
    return answer.replace(plaintext,b"")

# Returns the secret string used in the encryption function
# First do this manually to understand it and then implement this function
def crack(oracle,unknown_text_length):
    no_blocks = ceil(unknown_text_length/16)
    plaintext = b""
    result_string = b""
    append = b""

    for i in range(no_blocks):
        # length is 15 because 1 less than block size see comment below in loop
        ciphertext = oracle.encrypt("A"*15)
        # Need to append the known secret string block since it will be used for getting the next block of secret string
        plaintext = (b"A"*15) + result_string
        
        for j in range(16):
            temp = last_byte_crack(plaintext,ciphertext,oracle,i)
            result_string += temp
            if (14-j) >= 0:
                # Everytime the len(plaintext+result string) must be 1 less than multiple of block size
                # so that we can get the last byte using last byte crack function
                plaintext = plaintext[0:14-j] + result_string
                ciphertext = oracle.encrypt(plaintext[0:14-j])
            # print(result_string)
        
            if len(result_string)==unknown_text_length:
                break
    print("--------------Secret String used in Oracle-------------------")
    print(result_string.decode('ascii'))

def length_guess(oracle):
    plaintext = "A"
    cipher_len_prev = len(oracle.encrypt(plaintext))
    keysize = None

    for i in range(2,65):
        plaintext = "A"*i
        cipher_len = len(oracle.encrypt(plaintext))
        if(cipher_len>cipher_len_prev):
            keysize = cipher_len - cipher_len_prev
            break
    # The unknown text length is easy to calculate when our plaintext + that string exactly forms a string of multiples of keysize
    unknown_text_length = cipher_len_prev - (i-1)
    return (keysize,unknown_text_length)


if __name__=="__main__":
    oracle = AES128_Encryption_Oracle()

    _,unknown_text_length = length_guess(oracle)

    crack(oracle,unknown_text_length)
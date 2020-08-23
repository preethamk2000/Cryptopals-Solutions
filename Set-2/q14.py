import random
from os import urandom
import base64
from math import ceil
from q10 import AES_CBC,AES_ECB

class AES128_Encryption_Oracle2:
    
    def __init__(self):
        self.key = urandom(16)
        self.prepend = urandom( random.randint(5,100) )

    def preprocess(self,plaintext):
        prepend = self.prepend
        append = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
        append = base64.b64decode(append)
        # All are in bytes here
        plaintext = prepend + plaintext + append
        return plaintext
    
    def encrypt(self,plaintext):
        if type(plaintext)==str:
            plaintext = plaintext.encode('ascii')
        plaintext = self.preprocess(plaintext)

        enc_scheme = AES_ECB(self.key)
        
        ciphertext = enc_scheme.encrypt(plaintext)
        return ciphertext

# SEE Q12 BEFORE THIS, just add the prepended strings no of blocks to perform normally
# Gets the last byte of the block (or next byte of secret string) (block by block) by comparing it with all possible values of the last character's encryption by querying the oracle
def last_byte_crack(plaintext,ciphertext,oracle,iter,prepend_blocks):
    possible_vals = {}

    if type(plaintext)==str:
        plaintext = plaintext.encode('ascii')

    for i in range(128):
        # See q12 first, this is just a generalisation of that added with the prepend string
        val = oracle.encrypt(plaintext+bytes([i]))
        possible_vals[ val[ 16*iter+16*prepend_blocks : 16*(iter+1)+16*prepend_blocks ] ] = plaintext+bytes([i])
    
    # See q12 first
    answer = possible_vals[ciphertext[ 16*iter+16*prepend_blocks : 16*(iter+1)+16*prepend_blocks ] ]

    return answer.replace(plaintext,b"")

# See q12 first since this is an extension of it to include any length prepend string
# Returns the secret string used in the encryption function
def crack(oracle,unknown_text_length,prepend_blocks_occupied,prepend_bytes_to_a_block):
    no_blocks = ceil(unknown_text_length/16)
    default_a_count = 15+prepend_bytes_to_a_block
    plaintext = b""
    result_string = b""

    for i in range(no_blocks):
        ciphertext = oracle.encrypt("A"*default_a_count)
        plaintext = (b"A"*default_a_count) + result_string
        
        for j in range(16):
            temp = last_byte_crack(plaintext,ciphertext,oracle,i,prepend_blocks_occupied)
            result_string += temp
            if (default_a_count-1-j) >= 0:
                plaintext = plaintext[0:default_a_count-1-j] + result_string
                ciphertext = oracle.encrypt(plaintext[0:default_a_count-1-j])
            # print(result_string)
        
            if len(result_string)==unknown_text_length:
                break
    print("--------------Secret String used in Oracle-------------------")
    print(result_string.decode('ascii'))

# Gets the total prepended and appended string length
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
        # The below line is not actually needed.
        # cipher_len_prev = cipher_len

    # The unknown text length is easy to calculate when our plaintext + that string exactly forms a string of multiple of keysize
    unknown_text_length = cipher_len_prev - (i-1)
    return (keysize,unknown_text_length)

# THIS IS THE ONLY NEW FUNCTION NOT IN Q12
# Gets the prepended string length and its maximum block size and no of bytes to reach blocksize for further attack
def prepend_length_guesser(oracle):
    plaintext = "A"
    ciphertext_prev = oracle.encrypt(plaintext)
    no_of_blocks = int(len(ciphertext_prev)/16)
    
    # This range should be changed for AES > 128
    for i in range(2,20):
        plaintext = "A"*i
        ciphertext = oracle.encrypt(plaintext)

        # No of blocks occupied by the prepended string is (j+1)
        if i==2:
            for j in range(no_of_blocks):
                    if ( ciphertext_prev[16*j:16*(j+1)]!=ciphertext[16*j:16*(j+1)] ):
                        break
        
        # No of bytes left for the prepended string to complete block is (i-1)
        if(ciphertext_prev[16*j:16*(j+1)]==ciphertext[16*j:16*(j+1)]):
            break

        ciphertext_prev = ciphertext

    # Corrected i and j values if needed -> edge case when prepend length is either 16*k or 16*k-1
    if i-1 >= 16:
        i -= 16
        j -= 1 
    
    prepend_length = 16*(j+1)-(i-1)
    no_of_blocks_occupied = j+1
    no_of_bytes_less_than_blocksize = i-1

    return (prepend_length,no_of_blocks_occupied,no_of_bytes_less_than_blocksize)


if __name__=="__main__":
    oracle = AES128_Encryption_Oracle2()
 
    _,unknown_text_length_sum = length_guess(oracle)
    print("Sum of the length of prepended and appended strings : ",unknown_text_length_sum)

    prepend_length,a,b = prepend_length_guesser(oracle)
    print("----------Info about prepended string------------")
    print("Prepended string length:",prepend_length,"\nBlocks occupied:",a,"\nNo of bytes to reach blocksize:",b)
    crack( oracle, unknown_text_length_sum-prepend_length,a,b )
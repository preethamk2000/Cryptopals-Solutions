from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.backends import default_backend
from q9 import pkcs7_padding,pkcs7_padding_remove
import base64

class AES_ECB:

    backend = default_backend()

    def __init__(self,key):
        self.cipher = Cipher(algorithm=algorithms.AES(key),mode=modes.ECB(),backend=self.backend)
        self.keylen = len(key)
    
    def encrypt(self,plaintext):
        plaintext = pkcs7_padding(plaintext,self.keylen)
        encryptor = self.cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        return ciphertext
    
    def decrypt(self,ciphertext,final_block=False):
        decryptor = self.cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        if final_block==True:
            plaintext = pkcs7_padding_remove(plaintext,self.keylen)
        return plaintext


if __name__=="__main__":
    
    key = b"YELLOW SUBMARINE"
    plaintext = ""

    enc_scheme = AES_ECB(key)

    with open('7.txt','rb') as file:
        ciphertext = base64.b64decode(file.read())
        plaintext = enc_scheme.decrypt(ciphertext)

    print(plaintext.decode('utf-8'))

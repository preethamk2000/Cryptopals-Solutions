from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.backends import default_backend
import base64

class AES_ECB:

    backend = default_backend()

    def __init__(self,key):
        self.cipher = Cipher(algorithm=algorithms.AES(key),mode=modes.ECB(),backend=self.backend)
    
    def encrypt(self,plaintext):
        encryptor = self.cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        return ciphertext
    
    def decrypt(self,ciphertext):
        decryptor = self.cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext


if __name__=="__main__":
    
    key = b"YELLOW SUBMARINE"
    plaintext = ""

    enc_scheme = AES_ECB(key)

    with open('7.txt','rb') as file:
        ciphertext = base64.b64decode(file.read())
        plaintext = enc_scheme.decrypt(ciphertext)

    print(plaintext.decode('utf-8'))
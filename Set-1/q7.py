from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.backends import default_backend
import base64

backend = default_backend()

key = b"YELLOW SUBMARINE"
cipher = Cipher(algorithm=algorithms.AES(key),mode=modes.ECB(),backend=backend)

decryptor = cipher.decryptor()

plaintext = b""

# Here open mode can be 'r' or even 'rb'
with open('7.txt','rb') as file:
    plaintext += decryptor.update(base64.b64decode(file.read())) + decryptor.finalize()

print(plaintext.decode('utf-8'))
from random import getrandbits
from os import urandom
from q7 import AES_ECB

class profile:

    def __init__(self):
        self.key = urandom(16)
        # self.key = b"\xdf\x00\x85\x91\\\x9dJ\xd1\xda\x984\x05m\xd76\xd2"
        self.ecb_scheme = AES_ECB(self.key)

    def __parsing_routine(self,text):
        params = text.split("&")
        param_dict = {}

        for i in params:
            param = i.split("=")
            param_dict[param[0]] = param[1]
        
        return param_dict

    # Only for the "user" role
    def __profile_for(self,email):
        # Sanitizing inputs
        email = email.replace("&","").replace("=","") 

        encoding = ""
        params = []
        params.append("email=" + email)
        params.append("uid=10")
        params.append("role=user")

        for i in params:
            encoding += i + '&'
        
        encoding = encoding[0:len(encoding)-1]
        profile_dict = self.__parsing_routine(encoding)

        print("Expanded encoding for "+ email +": " ,profile_dict)
        return encoding

    def encrypt_encoding(self,plaintext):
        encoding = self.__profile_for(plaintext)
        encrypted_encoding = self.ecb_scheme.encrypt(encoding)
        return encrypted_encoding

    def decrypt_encoding(self,ciphertext):
        decrypted_encoding = self.ecb_scheme.decrypt(ciphertext)
        return decrypted_encoding


if __name__=="__main__":
    # Instantiate the class
    user_profile = profile()
    
    # Create an email such that the admin\x0b... thingy consumes a separate whole block in ECB
    # Since email=foo@bx.com is already a block
    email = "foo@bx.comadmin\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b"
    ciphertext = user_profile.encrypt_encoding(email)
    print("Value to Cut: ",ciphertext[16:32])
    admin_encrypted = ciphertext[16:32]

    # Now use another mail where email=fooo@baar.com&uid=10&role= is a multiple of blocksize so that user/admin comes in the last block 
    # This is the email to which we are going to forge the role to admin
    email2 = "fooo@baar.com"
    ciphertext2 = user_profile.encrypt_encoding(email2)

    print("----------Before changing----------")
    print(ciphertext)
    print(user_profile.decrypt_encoding(ciphertext2))
    # Now remove the user text at the end and add the encrypted admin block
    ciphertext2 = ciphertext2[0:32] + admin_encrypted
    decrypted_text2 = user_profile.decrypt_encoding(ciphertext2)
    print("-----------After changing------------\n")
    print("Changed ciphertext: ",ciphertext2,"\n","\nAfter changing role: ",decrypted_text2)
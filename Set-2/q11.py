from os import urandom
import random
from q10 import AES_CBC,AES_ECB

class AES_Encryption_Oracle:
    
    def __init__(self,keysize):
        self.key = urandom(keysize)
        # self.key = b"YELLOW SUBMARINE"
    
    def preprocess(self,plaintext):
        prepend = urandom( random.randint(5,10) )
        append = urandom( random.randint(5,10) )
        plaintext = prepend + plaintext + append
        return plaintext

    def choose_scheme(self):
        choice = random.random()
        if choice >= 0.5:
            return 2
        else:
            return 1
    
    def encrypt(self,plaintext):
        plaintext = plaintext.encode('ascii')
        plaintext = self.preprocess(plaintext)
        choice = self.choose_scheme()

        if choice == 1:
            # Do CBC scheme
            IV = urandom( random.getrandbits( len(self.key) ) )
            enc_scheme = AES_CBC(self.key,IV)
        else:
            # Do ECB scheme
            enc_scheme = AES_ECB(self.key)
        
        ciphertext = enc_scheme.encrypt(plaintext)
        return (ciphertext,choice)

def Oracle_guesser_check(ciphertext,choice):
    user_guess = None

    print("\n-----------Analysis From Guesser----------------")
    print(ciphertext[16:32])
    print(ciphertext[32:48])

    if ciphertext[16:32]==ciphertext[32:48]:
        user_guess = 2
    else:
        user_guess = 1
    
    if user_guess==choice:
        print("\nYeah boi! Correct guess from oracle guesser!")
    else:
        print("\nPathetic loser!")


if __name__=="__main__":
    # Here min length of this plaintext is 43 bytes inorder that there are atleast two blocks of A's
    # So using that we can distinguish b/w ECB and CBC
    plaintext = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

    oracle = AES_Encryption_Oracle(16)
    ciphertext,choice = oracle.encrypt(plaintext)
    print("-------Output From Oracle------------")
    print("Ciphertext: ",ciphertext,"\nChoice: ",choice)
    Oracle_guesser_check(ciphertext,choice)
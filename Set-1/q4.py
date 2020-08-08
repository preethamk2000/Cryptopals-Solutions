# import crypto_3
from q3 import *

with open("4.txt",'r') as file:
    with open('cryptofour.txt','w') as answers:
        line = file.readlines()
        for text in line:
            byteString = bytes.fromhex(text)
            for i in single_char_xor_attack(byteString):
                answers.write(i)
                answers.write("\n")

with open('cryptofour.txt','r') as file:
    lines = file.readlines()
    top10_scores = np.array([0.000000]*10)
    top10_text = ["text"]*10
    top10_ciphers = ["cts"]*10
    for text in lines:
        b_coef = np.min(top10_scores)
        freq = char_frequency(text)
        rho = bhattacharyya_coefficient(freq)
        if b_coef <= rho :
            # print(rho-b_coef)
            # b_coef = rho
            # print(plaintext,rho)
            ind = top10_scores.argmin()
            # print(ind)
            top10_scores[ind] = rho
            top10_text[ind] = text
        
    for i in np.argsort(top10_scores)[::-1]:
        print(">> "+top10_text[i])

# The resultant ct is : 7b5a4215415d544115415d5015455447414c155c46155f4058455c5b523f

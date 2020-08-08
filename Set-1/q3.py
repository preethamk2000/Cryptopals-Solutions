# Character frequency Finder

import numpy as np
from string import printable,ascii_lowercase
import matplotlib.pyplot as plt


# http://norvig.com/mayzner.html
ENGLISH_LETTER_FREQ = np.array([
   0.080398,  # a   
   0.014844,  # b 
   0.033450,  # c
   0.038164,  # d
   0.124933,  # e
   0.024021,  # f
   0.018689,  # g
   0.050540,  # h
   0.075683,  # i
   0.001599,  # j
   0.005416,  # k
   0.040690,  # l
   0.025115,  # m
   0.072344,  # n
   0.076413,  # o
   0.021355,  # p
   0.001206,  # q
   0.062803,  # r
   0.065132,  # s
   0.092745,  # t
   0.027304,  # u
   0.010523,  # v
   0.016753,  # w
   0.002357,  # x
   0.016640,  # y
   0.000897   # z
])

def bar_graph(xticks,y_vals,y_label,title,my_dpi=90,length=1200,breadth=800):

    plt.figure(figsize=(length/my_dpi, breadth/my_dpi), dpi=my_dpi)
    y_pos = np.arange(len(xticks))

    plt.bar(y_pos, y_vals)
    plt.xticks(y_pos, xticks)

    plt.ylabel(y_label)
    plt.title(title)

    # For the values on top
    for i, v in enumerate(y_vals.tolist()):
        plt.text(y_pos[i] - 0.3, v + 0.002, str(v)[2:6])

    plt.show()


# Refer https://crypto.stackexchange.com/questions/30209/developing-algorithm-for-detecting-plain-text-via-frequency-analysis
# https://www.scottbrady91.com/Cryptopals/Caesar-and-Vigenere-Ciphers

def bhattacharyya_coefficient(char_freq,eng_freq=ENGLISH_LETTER_FREQ):
    rho = np.sum(np.sqrt(np.multiply(char_freq,eng_freq)))
    # rho =np.multiply(char_freq,np.array(ENGLISH_LETTER_FREQ))
    # rho_mod = np.sqrt(1 - rho)
    # print(rho,rho_mod)
    return rho

def char_frequency(text):
    total = 0 
    char_count = np.array([0]*26)
    for t in text:
        if t.isalpha() :
            total = total + 1
            val = ord(t)
            if val <= 90 and val >=65: #FUCKIN PYTHON THINKS CHR(216) IS AN ALPHABET WTFH PYTHON ! :P
                char_count[val-65] = char_count[val-65] + 1
            elif val<=122 and val>= 97:
                char_count[val-97] = char_count[val-97] + 1 
    if total != 0:
        char_freq = char_count / float(total)
        return char_freq
    else:
        # print(text)
        return char_count

# This is to get the top 10 relevant english phrases
def single_char_xor_attack(byteString,keyOnly=False):
    top10_scores = np.array([0.000000]*10)
    # top10_text = [["text","key"]]*10 --> WRONG https://www.geeksforgeeks.org/python-using-2d-arrays-lists-the-right-way/
    top10_text = [['text' for i in range(2)] for j in range(10)] 

    # b_coef = 0
    # Here top10_text has the possible plaintext and its key and top10_scores has the corresponding score of those in top10_text
    for i in range(256):
        b_coef = np.min(top10_scores)
        plaintext = ""
        for j in byteString:
            plaintext = plaintext + chr(i^j)
        # plaintext = plain.decode('ascii')
        freq = char_frequency(plaintext)
        rho = bhattacharyya_coefficient(freq)
        if b_coef <= rho :
            # print(rho-b_coef)
            # b_coef = rho
            # print(plaintext,rho)
            index = top10_scores.argmin()
            # print(ind)
            top10_scores[index] = rho
            top10_text[index][0] = plaintext
            top10_text[index][1] = i #hex(i)
    
    # rtnString = ""

    # NEVER USE YIELD AND RETURN IN THE SAME FUNCTION UNNCESSARY CONFUSION
    if keyOnly == False:
        for i in np.argsort(top10_scores)[::-1]:
        # print(top10_text[i])
            yield " Key: " + str(top10_text[i][1]) + " " + top10_text[i][0]
        # rtnString += top10_text[i][0]+ " Key: " + str(top10_text[i][1]) + "|||\n"
    else:
        for i in np.argsort(top10_scores)[::-1]:
        # print(top10_text[i]) 
            yield top10_text[i][0]
        # rtnString += top10_text[i][1]
        # break


if __name__=="__main__":
    # Simply analysing char frequency in a valid English sentence.
    text = "Hello guys,my name is Preetham, you'll know me from my medium articles, I hope to continue writing as much as I can while learning!"
    freq = char_frequency(text)
    print(type(freq))
    bar_graph(list(ascii_lowercase),freq,"Frequency","Relative frequencies of alphabets in the given piece of text")
    xorStr = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    byteString = bytes.fromhex(xorStr)
    for i in single_char_xor_attack(byteString):
     print(i)
        
# BTW if you're confused about the achievement unlocked thingy: https://hci.stanford.edu/winograd/shrdlu/name.html
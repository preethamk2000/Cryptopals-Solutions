import numpy as np
import base64
from q3 import bhattacharyya_coefficient,char_frequency,single_char_xor_attack

# https://crypto.stackexchange.com/questions/8115/repeating-key-xor-and-hamming-distance
def hamming_distance(str1,str2,encoding='ascii'): # also called edit distance I guess 
    if(len(str1)!=len(str2)):
        return -1
    # str1 = str1.encode(encoding)
    # str2 = str2.encode(encoding)
    count = 0
    for i in range(len(str1)):
        # print(str1[i])
        count = count + bin(str1[i]^str2[i]).count('1')
    return count

# a = hamming_distance('this is a test','wokka wokka!!!')
# print(a)

def key_size_guesser(text,msize=2,Msize=40):
    min6_hvals = np.array([999999.000]*10)
    min6_keysize = [0]*10
    for i in range(msize,Msize+1):
        h_max = np.max(min6_hvals)
        max_blocks = int(len(text)/i)
        if max_blocks <= 1 :
            break
        else:
            hcode = 0.0000
            for j in range(1,max_blocks):
                hcode = hcode + hamming_distance(text[(j-1)*i:j*i],text[j*i:(j+1)*i])
            avg = hcode/(float(i)*(max_blocks-1))
        if h_max >= avg:
            ind = min6_hvals.argmax()
            min6_hvals[ind] = avg
            min6_keysize[ind] = i
    print(min6_keysize,min6_hvals)
    return min6_keysize

# WORKS
def actual_repeating_xor(ciphertext,keylen):
    # no_of_blocks = int(len(ciphertext)/keylen)
    blocks = []
    key = ""
    for i in range(keylen):
        blocks.append(ciphertext[i::keylen])
        for k in single_char_xor_attack(blocks[i],True):
            key += chr(k)
            break
        # key += "  !#END#!\n"
    print(key)
    print("======================================================================\n")


# FOR NOW THIS IS JUST A DUMMY FUNCTION AS IM NOT SURE HOW TO HANDLE 2D STRINGS GRACEFULLY WITH NUMPY
def multi_xor_crack(texts_map,keylen):
    blocks = int(len(texts_map[0][0])/keylen)
    # print(texts_map[0][0])
    letters = [[-1 for i in range(texts_map.size*blocks)] for j in range(keylen)]
    # https://stackoverflow.com/questions/13717554/weird-behaviour-initializing-a-numpy-array-of-string-data
    count = 0
    # block_map = np.empty((texts_map.shape[0],blocks),dtype='S'+str(keylen))
    block_map = np.empty((texts_map.shape[0],blocks),dtype=object)
    for i in range(block_map.shape[0]):
        # declare as dtype object since some \x00 chrs are being trimmed if dtype is string
        sub_block = np.array( [texts_map[i][0][k:k+keylen] for k in range(0, len(texts_map[i][0]), keylen)],dtype=object )
        for j in range(block_map.shape[1]):
            print(i)
            block_map[i] = sub_block
            # print(i,j)
            # print(block_map[0])
            # print(block_map[i][j][7])
            for k in range(keylen):
                # print(i,j,k)
                letters[k][count] = block_map[i][j][k]
                # print(block_map[i][j][k])
            count = count + 1
    return letters
    # block_map[0] = np.array(["hello","hey","yo","hi","ho"]) 
    # print(len(texts_map[0]))
    # print(block_map[16])
    
# THE BELOW SHIT IS FROM TRYING TO IMPLEMENT THE MULTI XOR CRACK FUNCTION

# text = bytes.fromhex("00100403451113001b46031814451107091b0f0b1046031b09061c15").decode('ascii')
# text = "00100403451113001b"
# print(type(text))
# key_size_guesser(text)

# poss_keysize = np.array([0]*40)

# texts_map = np.empty((64,1),dtype=object)
# count = 0
# with open('6.txt','r') as file:
#     ciphertext = base64.b64decode(file.read())
    # lines = file.readlines()
    # for line in lines:
    #     text = base64.b64decode(line)
    #     texts_map[count] = text
    #     count = count + 1
# print(ciphertext[::1])

# texts_map[63][0] += b'\x00\x00\x00\x00' # to adjust padding issues wi
# letters = multi_xor_crack(ciphertext,29)
# byteString = ciphertext[28::29]
# for i in single_char_xor_attack(byteString):
#     print(i)
#     break

# string = texts_map[63][0] 
# print(string)
# alist = [texts_map[63][0][k:k+9] for k in range(0, len(texts_map[63][0]), 9)]
# print(alist)

# anskey = b"Terminator X: Bring the noise"

if __name__=="__main__":
    with open('6.txt','r') as file:
        ciphertext = base64.b64decode(file.read())
        # THE METHOD USED HERE FOR CALCULATING KEYS IS VERY LESS ACCURATE I GUESS ~30% ACC TO WHAT IVE READ
        # https://trustedsignal.blogspot.com/2015/06/xord-play-normalized-hamming-distance.html
        # BUT IT WORKS FOR THE GIVEN TASK SO xD
        # del ciphertext
        # ciphertext = bytes.fromhex("00100403451113001b46031814451107091b0f0b1046031b09061c15")
        print("-------------Possible key sizes and their scores:----------------")
        keys = key_size_guesser(ciphertext)

        print("-------------Possible keys for each length:----------------")
        for i in keys:
            print("Key size: "+str(i))
            actual_repeating_xor(ciphertext,i)

        # This below is the one which we got from my code, but if you fix the upper/lower case errors, you get the whole decrypted poem
        # anskey_string = "TERmInAtor x: brIng The noIse"
        actual_anskey = b"Terminator X: Bring the noise"
        # anskey = anskey_string.encode('utf-8')
        anskey = actual_anskey
        count = 0
        plaintext = ""

        for i in ciphertext:
            plaintext += chr( i ^ anskey[count%len(anskey)] )
            count += 1
        
        print("-----------------THE DECRYPTED TEXT:-------------------------")
        print(plaintext)
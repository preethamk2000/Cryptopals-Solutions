with open('8.txt','r') as file:
    lines = file.readlines()

    for line in lines:
        no_of_blocks = int(len(line)/16)

        for i in range(no_of_blocks):
            block = line[16*i:16*(i+1)]
            count = line.count(block)
            if count > 1:
                print("Repetition found:")
                print(block)
                print(line)
                break

# A better way is to use sets in Python:
# Or even frozensets in our case here
# https://www.geeksforgeeks.org/frozenset-in-python/
# https://cedricvanrompay.gitlab.io/cryptopals/challenges/01-to-08.html

#     blocks = [ctxt[i*blocksize:(i+1)*blocksize] for i in range(num_blocks)]
    
#     if len(set(blocks)) != num_blocks:      --> Set is used here
#         return True
#     else:
#         return False

# ANSWER IS THE ONE BELOW
# "d880619740a8a19b7840a8a31c810a3d08649af70dc06f4fd5d2d69c744cd283e2dd052f6b641dbf9d11b0348542bb5708649af70dc06f4fd5d2d69c744cd2839475c9dfdbc1d46597949d9c7e82bf5a08649af70dc06f4fd5d2d69c744cd28397a93eab8d6aecd566489154789a6b0308649af70dc06f4fd5d2d69c744cd283d403180c98c8f6db1f2a3f9c4040deb0ab51b29933f2c123c58386b06fba186a"
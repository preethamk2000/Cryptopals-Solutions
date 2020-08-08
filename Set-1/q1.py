import base64

hexString = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

byteString = bytes.fromhex(hexString)

# bytes.fromhex(hex_string) OR bytearray.fromhex(hex_string) 
# Note that bytes is an immutable version of bytearray.

print(byteString)

# b64String = byteString.b64decode() WRONG since b64 converts bytearray and groups them differently (say from 8bits to 6bits) 
# and then maps them to a b64 character then converts that to its ascii value finally returning them as a bytearray 
# Thus say you have a 24bit string ,ie 3 letters when they are b64encoded ans: 32bits for others you need to take care of padding and removing leading 0's in binary
b64String = base64.b64encode(byteString)

# base64.b64encode
print(b64String)
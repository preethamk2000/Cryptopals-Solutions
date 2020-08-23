from q9 import pkcs7_padding_remove
import sys

def pkcs7_padding_validator(padded_text,blocksize=8):
    lastchar_int = padded_text[-1]
    text = pkcs7_padding_remove(padded_text,blocksize)
    if(padded_text==text):
        print("No need to remove padding!")
        return True
    else:
        if len(padded_text)-len(text) != lastchar_int:
            return False
        else:
            for i in range(lastchar_int-1):
                if lastchar_int!=padded_text[-(i+2)]:
                    return False
            return True

def actual_validator(padded_text,blocksize=8):
    val = pkcs7_padding_validator(padded_text,blocksize)
    
    if val==True:
        print("Correct padding!")
    else:
        # Simple exceptions are enough for now
        raise Exception("Incorrect padding detected!")


if __name__=="__main__":
    padded_text = "ICE ICE BABY\x01\x02\x03\x04".encode()
    actual_validator(padded_text,16)
from binascii import b2a_hex, a2b_hex
from Crypto.Cipher import DES
import sys

#key = '12345678'

while 1:
    key = raw_input('Please input the key(8 bytes): ')
    if key == '12345678':
        file = open('history', 'r')
        try:
            text = file.read()
        finally:
            file.close()

        obj = DES.new(key)
        get_cryp = a2b_hex(text)
        after_text = obj.decrypt(get_cryp)
        print '\nChat History: \n' + after_text
        break;
    else:
        result = raw_input("Wrong!Input anything try again!(If you won't try another time, just input 'no') Your Answer is: ")
        if result == 'no':
            break;

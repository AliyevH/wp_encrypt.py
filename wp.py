# Credits go to:
# https://www.facebook.com/permalink.php?id=120707754619074&story_fbid=389700354386478
# Fixed spacing (posting python on facebook is gr8 idea guys)
# Added generating passwords.

from hashlib import md5
import random
import base64
itoa64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def encode64(textInput,count):
    output = ''
    i = 0
    while i < count:
        i = i + 1
        value = textInput[i-1]
        output = output + itoa64[value & 63]
        
        if i < count :
            value = value | (textInput[i] << 8)
        output = output + itoa64[(value >> 6) & 63]
        
        if i >= count:
            break
        i += 1

        if i < count:
            value = value | (textInput[i] << 16)
            output = output + itoa64[(value >> 12) & 63]
            i = i + 1
        if i >= count:
            break
        output = output + itoa64[(value >> 18) & 63]
     

    return output


def crypt_private(password, setting=None):
	
    output = '*0' # old type | not supported yet
    if setting[0:2] == output:
        output = '*1'
    id = setting[0:3]
    if id != '$P$' and id != '$H$': # old type | not supported yet
        return output

    # get who many times will generate the hash
    count_log2 = itoa64.find(setting[3])
    
    if (count_log2 < 7) or (count_log2 > 30):
        return output

    count = 1 << count_log2 # get who many times will generate the hash
    
    salt = setting[4:12] # get salt from the wordpress hash
    if len(salt) != 8:
        return output
    # generate the first hash from salt and word to try

    _hash = md5(str.encode(str(salt)+str(password))).digest()
    
    for i in range (count):
        # regenerate the hash
        _hash = md5(_hash + str.encode(password)).digest()
    output = setting[0:12]
    # get the first part of the wordpress hash (type,count,salt)
    output = output + encode64(_hash,16) # create the new hash

    return output

def check(password, hashed_password):
    ss = crypt_private(password, hashed_password)
    return ss == hashed_password


print(check('1234567', '$P$BnGMTITMl1I3aXfqDtlonOODdBoEvx0'))

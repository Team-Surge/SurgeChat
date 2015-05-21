import os
import string
import random
from Crypto.Cipher import AES

#generate random string
def randomMsg(size = 10, chars = string.ascii_letters + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

randomMsg = randomMsg(128)
print randomMsg

#NOTE: for AES, the password MUST be 16 bytes long, and the IV must be 16 bytes long

aesKey = 'Sur9e 1s d b3ST!'
aesIV = 'ouR 1v is super!'

# Encryption
encryption_suite = AES.new(aesKey, AES.MODE_CBC, aesIV)
cipher_text = encryption_suite.encrypt(randomMsg)

# Decryption
decryption_suite = AES.new(aesKey, AES.MODE_CBC, aesIV)
plain_text = decryption_suite.decrypt(cipher_text)

print cipher_text
print
print plain_text

if plain_text == randomMsg:
  print 'Response to challenge successful, you are authorized'




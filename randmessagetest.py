import os
import string
from surgeUtilities import *
import base64
from Crypto.Cipher import AES

randomMsg = randomMsg(128)
print randomMsg

#NOTE: for AES, the password MUST be 16 bytes long, and the IV must be 16 bytes long


#=========SURGE SERVER SIDE=========#
aesKey = 'Sur9e 1s d b3ST!'
aesIV = 'ouR 1v is super!' #Tom will randomly generate a 16byte IV string, and send it to me along with the encrypted response, I'll use it for decryption

# Encryption
encryption_suite = AES.new(aesKey, AES.MODE_CBC, aesIV)
cipher_text = encryption_suite.encrypt(randomMsg)
cipher_base64 = base64.b64encode(cipher_text)

#=========CHAT SERVER SIDE=========#
# Tom needs to send the encrypted data to me over the network, so he will need to base64 encode the 
# result of his encryption. I'll base64 decode the original encrypted message on my end, and then
# decrypt the aes encrypted message using the IV string tom will also send along with it
print cipher_text
print cipher_base64

# Decryption
decryption_suite = AES.new(aesKey, AES.MODE_CBC, aesIV)
plain_text = decryption_suite.decrypt(base64.b64decode(cipher_base64))

print plain_text

if plain_text == randomMsg:
  print 'Response to challenge successful, you are authorized'




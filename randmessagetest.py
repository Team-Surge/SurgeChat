import string
import random

#generate random string
def randomMsg(size = 10, chars = string.ascii_letters + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

print randomMsg(128)

import hashlib

BUF_SIZE = 65536 # lets read stuff in 64kb chunks!

"""
md5 hash of file
"""
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(BUF_SIZE), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

"""
sha1 hash of file    
"""
def sha1(fname):
    hash_sha1 = hashlib.sha1()
    with open(fname, 'rb') as f:
       for chunk in iter(lambda: f.read(BUF_SIZE), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()


import random
import string

"""
Return a random alphanumerical id
"""
def random_id(length = 10):
  rid = ''
  for x in range(length): rid += random.choice(string.ascii_letters + string.digits)
  return rid

"""
Return a random alphanumerical id
"""
def random_id_mod(length = 10, strong = False):
  rid = ''
  for x in range(length):
    rid += random.choice(('!@#$%^&*()_-+=' if strong else '') + string.ascii_letters + string.digits)
  return rid

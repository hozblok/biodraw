import hashlib

BUFF_SIZE = 65536

def _hashing(file_name, hash_object, buff_size=BUFF_SIZE):
        with open(file_name, 'rb') as file:
                for chunk in iter(lambda: file.read(buff_size), b""):
                        hash_object.update(chunk)
        return hash_object.hexdigest()
        
def _hashing_django_uploaded_file(f, hash_object, buff_size=BUFF_SIZE):
        for chunk in f.chunks(BUFF_SIZE):
            hash_object.update(chunk)
        return hash_object.hexdigest()

"""
sha1 hash of file    
"""	
def sha1(fname):
    return _hashing(fname, hashlib.sha1())

"""
md5 hash of file
"""	
def md5(fname):
    return _hashing(fname, hashlib.md5())
    
"""
sha1 hash of object of class UploadedFile
"""	
def sha1_uploaded_file(object_file):
    return _hashing_django_uploaded_file(object_file, hashlib.sha1())

"""
md5 hash of object of class UploadedFile
"""	
def md5_uploaded_file(object_file):
    return _hashing_django_uploaded_file(object_file, hashlib.md5())


import random
import string

"""
Return a random alphanumerical id
"""
def random_id(length=10, strong=False):
    rid = ''
    alphabet = ('!@#$%^&*()_-+=' if strong else '') + string.ascii_letters + string.digits
    for x in range(length):
        rid += random.choice(alphabet)
    return rid

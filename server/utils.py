import M2Crypto
import string

def random_password(length=10):
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    password = ''
    for i in range(length):
        password += chars[ord(M2Crypto.m2.rand_bytes(1)) % len(chars)]
    return password
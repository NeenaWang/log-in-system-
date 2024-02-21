from hashlib import sha256, pbkdf2_hmac
from random import getrandbits

PERFORMANCE_STATS = {
    "random_salt": 0,
    "hash_sha": 0,
    "hash_pbkdf": 0 }

# Generate 128-bit random salt as string of hex values
def random_salt():
    PERFORMANCE_STATS["random_salt"] += 1
    return getrandbits(128).to_bytes(16, byteorder='little').hex()


# Input: string; Output: string of hex values
def hash_sha256(x):
    PERFORMANCE_STATS["hash_sha"] += 1
    return sha256(x.encode('utf-8')).hexdigest()


# Input: string x and string of hex salt; Output: string of hex values
def hash_pbkdf2(x, salt):
    PERFORMANCE_STATS["hash_pbkdf"] += 1
    return pbkdf2_hmac('sha256', x.encode('utf-8'), bytes.fromhex(salt), 100000).hex()


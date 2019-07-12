import random
import string
import hashlib


def randomword(length=8):
    char_set = string.ascii_lowercase + string.digits + string.ascii_uppercase
    return ''.join(random.choice(char_set) for i in range(length))


def permanent_hash(o):
    """
    Implements a hashing that is constant across sessions.
    :param o: the object to be encoded
    :return: a string representation
    """
    return hashlib.md5((str(o)).encode()).hexdigest()

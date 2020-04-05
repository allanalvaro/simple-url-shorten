import random
import string


def generate_hash(size: int):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(size))

import random
import string


def generate_hash():
    letters = string.ascii_lowercase
    print(letters)
    return ''.join(random.choice(letters) for i in range(6))
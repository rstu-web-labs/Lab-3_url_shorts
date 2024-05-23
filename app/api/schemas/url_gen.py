import random
import string


def generate_short_url(max_length: int):
    return ''.join(random.choice(string.ascii_letters) for i in range(random.randint(4, max_length)))

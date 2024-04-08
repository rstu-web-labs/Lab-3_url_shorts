import random
import string

def generate_short_link():
    characters = string.ascii_letters + string.digits
    short_link = ''.join(random.choices(characters, k=8))
    return 'https://' + short_link
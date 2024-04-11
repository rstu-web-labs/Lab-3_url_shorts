import random
import string

def CreateShortLink():
    characters = string.ascii_letters + string.digits
    shortLink = ''.join(random.choices(characters, k=8))
    return 'https://' + shortLink
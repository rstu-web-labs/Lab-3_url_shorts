import logging
import re

def CheckUrl(url):
    logging.info(f"Variable to log: {url}")
    pattern = "^(https?|ftp|file)://[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]"
    if re.match(pattern, url):
        return True
    else:
        return False
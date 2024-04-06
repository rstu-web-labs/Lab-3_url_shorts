import logging
import re


def validate_url(url):
    logging.info(f"Variable to log: {url}")
    regex_pattern = "^(https?|ftp|file)://[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]"
    if re.match(regex_pattern, url):
        return True
    else:
        return False

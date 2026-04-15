import re

def is_ascii(s: str) -> bool:
    indian_script_patterns = [
        r'[\u0900-\u097F]',  # Devanagari
        r'[\u0B80-\u0BFF]',  # Tamil
        r'[\u0C00-\u0C7F]',  # Telugu
        r'[\u0C80-\u0CFF]',  # Kannada
        r'[\u0D00-\u0D7F]',  # Malayalam
        r'[\u0A80-\u0AFF]',  # Gujarati
        r'[\u0A00-\u0A7F]',  # Gurmukhi
        r'[\u0980-\u09FF]',  # Bengali / Assamese
        r'[\u0B00-\u0B7F]',  # Odia
    ]
    for pattern in indian_script_patterns:
        if re.search(pattern, s):
            return False
    return all(ord(c) < 128 for c in s if c.isalpha())
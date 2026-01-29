def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    keyword_len = len(keyword)
    for i, char in enumerate(plaintext):
        if 'A' <= char <= 'Z':
            base = ord('A')
            key_char = keyword[i % keyword_len].upper()
            shift = ord(key_char) - base
            new_code = (ord(char) - base + shift) % 26 + base
            ciphertext += chr(new_code)
        elif 'a' <= char <= 'z':
            base = ord('a')
            key_char = keyword[i % keyword_len].lower()
            shift = ord(key_char) - base
            new_code = (ord(char) - base + shift) % 26 + base
            ciphertext += chr(new_code)
        else:
            ciphertext += char
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    keyword_len = len(keyword)
    for i, char in enumerate(ciphertext):
        if 'A' <= char <= 'Z':
            base = ord('A')
            key_char = keyword[i % keyword_len].upper()
            shift = ord(key_char) - base
            new_code = (ord(char) - base - shift) % 26 + base
            plaintext += chr(new_code)
        elif 'a' <= char <= 'z':
            base = ord('a')
            key_char = keyword[i % keyword_len].lower()
            shift = ord(key_char) - base
            new_code = (ord(char) - base - shift) % 26 + base
            plaintext += chr(new_code)
        else:
            plaintext += char
    return plaintext
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
    plaintext_upper = plaintext.upper()
    keyword_upper = keyword.upper()
    for i, char in enumerate(plaintext):
        if char.isalpha():
            plain_index = ord(plaintext[i].upper()) - ord('A')
            key_index = ord(keyword_upper[i % len(keyword_upper)]) - ord('A')
            cipher_index = (plain_index + key_index) % 26
            ciphertext += chr(cipher_index + ord(char.isupper() and 'A' or 'a'))
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
    ciphertext_upper = ciphertext.upper()
    keyword_upper = keyword.upper()
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            cipher_index = ord(ciphertext[i].upper()) - ord('A')
            key_index = ord(keyword_upper[i % len(keyword_upper)]) - ord('A')
            plain_index = (cipher_index - key_index) % 26
            plaintext += chr(plain_index + ord(ciphertext[i].isupper() and 'A' or 'a'))
        else:
            plaintext += char
    return plaintext
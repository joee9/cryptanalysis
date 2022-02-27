# Joe Nyhan, 15 February 2022

# Decrypts a Vigenere Cypher given input text file and keyword.

# ========== TEXT RELATED

def letter_idx(c:str):
    """
    returns the index (0-25) of any upper or lowercase letter
    """
    assert type(c) == str   # must be a string
    assert c.isalpha()      # all alphanumeric
    assert len(c)           # c must be a single letter

    return ord(c.upper()) - ord('A')

def filter_text(text:str):
    """
    turns any string of text into a string of just the uppercase letters
    """
    assert type(text) == str

    text = list(filter(str.isalpha, text))
    text = ''.join(text).upper()
    return text


def get_text(filename:str) -> str:
    """
    retrieve and filter text from filename
    """
    if not '.txt' in filename:
        filename += '.txt'

    with open(filename, 'r') as f:
        s = f.read()
    
    return filter_text(s)

# ========== ALGORITHMS

def calc_key_shifts(key):
    """
    return an array of the letter indices of the key
    """
    shifts = []
    for c in key:
        shifts.append(letter_idx(c))
    
    return shifts

def decrypt_vigenere(cypher_text, key):
    
    # if this is true, probably a filtered statement, should be in the clear
    assert cypher_text.isalpha()

    shifts = calc_key_shifts(key)
    
    n = len(key)
    plain_text = ''
    
    for i,c in enumerate(cypher_text):
        ci = letter_idx(c)
        idx = i % n
        if ci < shifts[idx]: ci += 26

        dec = ci - shifts[idx]

        plain_text += chr(dec + ord('A'))

    return plain_text

def encrypt_vigenere(plain_text, key):
    
    # if this is true, probably a filtered statement, should be in the clear
    assert plain_text.isalpha()

    shifts = calc_key_shifts(key)
    
    n = len(key)
    cypher_text = ''

    for i,c in enumerate(plain_text):
        ci = letter_idx(c)
        idx = i % n

        enc = (ci + shifts[idx]) % 26

        cypher_text += chr(enc + ord('A'))

    return cypher_text


def main():

    # ========== PARAMETERS

    decrypt = 1
    encrypt = 0
    test    = 0

    # file = 'cipherKnownKey.txt'
    file = 'cipherNoKey.txt'

    # key = 'tagore'
    key = 'marktwain'

    assert key.isalpha()

    # ========== ACTUAL CODE

    text = get_text(file)

    if decrypt:
        if '.txt' in file:
            file = file.replace('.txt','')
            file = file + '-decrypt.txt'
        else:
            file = file + '-decrypt.txt'

        with open(file,'w') as out:
            out.write(decrypt_vigenere(text, key))

    if encrypt:
        if '.txt' in file:
            file = file.replace('.txt','')
            file = file + '-encrypt.txt'
        else:
            file = file + '-encrypt.txt'

        with open(file,'w') as out:
            out.write(encrypt_vigenere(text, key))
    
    if test:
        filtered_text = filter_text(text)
        test_text = decrypt_vigenere(encrypt_vigenere(text, key),key)
        print(filtered_text == test_text)
    
if __name__ == '__main__':
    main()
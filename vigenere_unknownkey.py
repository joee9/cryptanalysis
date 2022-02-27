# Joe Nyhan, 16 February 2022

# Decrypts a text encoded with Vigenere cypher when keyword is unknown.

from vigenere_knownkey import decrypt_vigenere, get_text
from nltk.corpus import words

# ========== GLOBAL PARAMETERS

english_kws             = 0
print_ioc_table         = 1
print_text_first_part   = 1
print_kws               = 1
smallest_kw_length      = 1
most_likely_word        = 0
kws_as_set              = 0
include_T_shift         = 0

user_analysis           = 0

num_letters             = 3

assert 1 <= num_letters <= 26

# ========== LETTER AND TEXT RELATED

def get_letter_frequencies(s):
    """
    for an inputted string, return a dictionary containing the frequencies
    of each captial english letter
    """

    assert s.isalpha() and s.isupper() # must be alphanumeric and uppercase

    # initialize every letter to a ct of zero within dictionary
    freqs = {}
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for c in letters:
        freqs[c] = 0
    
    # add all frequencies to dictionary
    for c in s:
        freqs[c] += 1

    return freqs

def split_text(text, n):
    """
    split text into $n$ subtexts at every $n$th character
    """
    subtexts = []
    for i in range(n):
        subtexts.append('')
    
    for i,c in enumerate(text):
        idx = i % n
        subtexts[idx] += c
    
    return subtexts

# ========== KEY LENGTH RELATED

def calc_ioc(s):
    """
    for an inputted string, will calculate the IoC of the text.
    """

    assert s.isalpha() and s.isupper() # must be alphanumeric and uppercase

    n = len(s)
    if n <= 1: return 0

    freqs = get_letter_frequencies(s)
    # print(freqs)

    total = 0
    for c in freqs.keys():
        ct = freqs[c]
        total += (ct)*(ct-1)

    ioc = total/(n*(n-1))

    return ioc


def find_key_length(text):
    """
    given a text, will return a list of possible key lengths;
    also, prints ioc table if specificed by global param
    """
    upper_bound = 11
    possible_lengths = []
    # for i in range(1,21): # check all key lengths up to 20 characters
    if print_ioc_table:
        print('IOC TABLE')
        print(f'  len  ', end='')
        for i in range(1,upper_bound):
            print(f'{i:^5d} ', end='')
        print('')

    av_iocs = {}
    for i in range(2,upper_bound): # check all key lengths up to 10 characters
        sym = '  '
        iocs = []
        texts = split_text(text, i)
        for t in texts:
            iocs.append(calc_ioc(t))
        
        # if all iocs of subtexts are greater than .6, we assume that this
        #   text likely has the same letter frequency as English
        ioc_in_range = [ioc > .059 for ioc in iocs]
        av_ioc = sum(iocs)/len(iocs)
        if all(ioc_in_range):
            possible_lengths.append(i)
            sym = '->'
        
        av_iocs[av_ioc] = i

        if print_ioc_table:
            print(f'{sym}{i:3d}: ', end='') 
            for ioc in iocs:
                print(f'{ioc:.3f} ', end='')
            print('')
    
    if print_ioc_table: 
        print('Possible lengths: ', end='')
        print(possible_lengths)
        print('')
    
    if smallest_kw_length: 
        if possible_lengths == []:
            k = max(av_iocs.keys())
            possible_lengths = [av_iocs[k]]
        else:
            possible_lengths = [possible_lengths[0]]

    return possible_lengths


def get_most_freq_letters(freqs):
    """
    from freqencies, get most frequent letter
    """
    freq_items = freqs.items()

    def sort_procdeudre(item):
        return -item[1]

    sort = sorted(freq_items, key=sort_procdeudre)
    
    letters = []
    for item in sort:
        letters.append(item[0])

    if user_analysis:
        return letters
    else:
        return letters[0:num_letters]


def get_keyword_letters(text):
    """
    from text, map most frequent letter to both e and t and return
    those letters
    """

    freqs = get_letter_frequencies(text)
    ls = get_most_freq_letters(freqs)
    kw_letters = []

    for l in ls:

        E_shift = (ord(l) - ord('E') + 26) % 26
        kw_letters.append(chr(E_shift + ord('A')))

        if include_T_shift:
            T_shift = (ord(l) - ord('T') + 26) % 26
            kw_letters.append(chr(T_shift + ord('A')))

    return kw_letters


def filter_kws(list):
    """
    based on global param english_kws, will filter list of kws
    """

    if most_likely_word:
        return [list[0]]

    if kws_as_set:
        list = set(list)

    if not english_kws:
        return list

    kws = []
    for i,key in enumerate(list):
        # if i % 25: print(i)
        if key.lower() in words.words():
            kws.append(key)

    return kws


def create_kws(list):
    """
    recursively create a list of all possible keywords from a 2D list of characters;
    one character taken from each element in the major axis
    """

    kws = []
    n = len(list) # essentially length of kw

    def kw_helper(chars, idx, length, word, words):
        if idx == length-1:
            for c in chars[idx]:
                words.append(word + c)
            return

        for c in chars[idx]:
            kw_helper(chars, idx + 1, length, word + c, words)
        
    kw_helper(list, 0, n, '', kws)
    
    return filter_kws(kws)

def run_vigenere_decrypt(text, key):
    print(f'Keyword = {key}')
    print(f'Plain text:')
    plain_text = decrypt_vigenere(text,key)
    if print_text_first_part:
        length = 77
        pt_len = len(plain_text)
        if pt_len < length: length = pt_len
        plain_text = plain_text[0:length] + '...'
    print(plain_text)
    print('')

def decrypt_text(text):

    print('Cipher text:')
    print(text)
    print('')

    # text must be filtered before it is used
    assert text.isalpha() and text.isupper()

    key_lengths = find_key_length(text)

    for n in key_lengths:

        texts = split_text(text, n)
        kw_letters = []
        for t in texts:
            kw_letters.append(get_keyword_letters(t))
        
        for item in kw_letters:
            print(item)
        print('')

        if not user_analysis:
            kws = create_kws(kw_letters)
            
            if print_kws:
                print('Number of Keywords: ' + str(len(kws)))
                print(kws)
                print('')

            for key in kws:
                run_vigenere_decrypt(text,key)
        else:
            key = ''.join([item[0] for item in kw_letters])
            print(f'Most likely key: {key}')
            run_vigenere_decrypt(text,key)

            # cycle while user guesses keys
            while True:
                # print out letters
                for item in kw_letters:
                    print(item)
                print('')           

                key = input('Please input a key: ')

                if key == 'n' or key == 'N' or key == 'Exit': break

                # fill out key with most common letters
                if len(key) < n:
                    to_add = n-len(key)
                    for i in range(len(key),len(key)+to_add):
                        key = key+kw_letters[i][0]

                run_vigenere_decrypt(text,key)

def main():
    file = './cipherNoKey.txt'      # key = 'marktwain'

    text = get_text(file)
    decrypt_text(text)

if __name__ == '__main__':
    main()
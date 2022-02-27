# Joe Nyhan, 19 February 2022

# Decrypts a LSFR encrypted file given an initial
#   fill and recursive function.

from bitarray import bitarray

def generate_next_bit(key):
    """
    calculates the next bit in the key given the current key (fill)
    """
    # recursive function is a_n = a_{n-4} + a_{n-5} + a_{n-6} + a_{n-8}

    a4 = key[-4]
    a5 = key[-5]
    a6 = key[-6]
    a8 = key[-8]

    return (a4 + a5 + a6 + a8) % 2

def calculate_key(n, fill:str, key):
    for c in fill:
        key.append(int(c))
    for i in range(len(fill), n):
        key.append(generate_next_bit(key))

def calculate_message(message, stream, key):
    for i in range(len(stream)):
        b = stream[i] ^ key[i]
        message.append(b)

def decrypt_stream_cipher(file, str_fill:str, ext):

    with open(f'{file}.encrypted','rb') as f:
        stream_bytes = f.read()
    
    print('Input Stream:')
    print(stream_bytes.hex()[0:100])
    stream = bitarray()
    stream.frombytes(stream_bytes)
    
    key = bitarray()
    calculate_key(len(stream), str_fill, key)
    print(key[0:100])

    message = bitarray()
    calculate_message(message, stream, key)

    decrypted_message = message.tobytes()
    print('Output Stream:')
    print(decrypted_message.hex()[0:100])
    
    with open(file + f'-decrypted.{ext}','wb') as f:
        f.write(decrypted_message)
    
    with open('./key.bin', 'wb') as f:
        f.write(key)

    with open(file + f'.decrypted','wb') as f:
        f.write(decrypted_message)


def main():
    fill = '11111111'
    file = 'LFSR' # .encrypted is implicit
    ext = 'jpg'

    decrypt_stream_cipher(file, fill, ext)

if __name__ == '__main__':
    main()


# Cryptoanalysis Software/Encryption-Decryption Algorithms
For College of the Holy Cross, CSCI 399: Computer Security, Project 1; see project specifications in `p1-questions.pdf`.

This repository contains three files, each with a different purpose.

1. `vigenere_knownkey.py` will encrypt and decrypt text using a Vigenere cipher with a specified key. Place the file name of the input text (encrypted or decrypted) in `file` in `main()`, present a key, and an output file will be written. An example is given in `cipherKnownKey.txt`, with the decrypted file in `cipherKnownKey-decrypt.txt`, given the key "TAGORE".

2. `vigenere_unknownkey.py` is a cryptoanalysis program written to analyze an input text, known to be encrypted using a Vigenere cipher, but with no knowledge of the key. Will determine the key length, the most probable keyword, and will print various decrypted texts to file for the user to analyze. See sample output, for the encrypted file `cipherNoKey.txt`, in `vigenere_unknownkey-output.txt`.

3. `LFSR_decrypt.py` will decrypt a file encrypted with a LFSR, given an initial fill and recursive function. Uses the `bitarray` data structure for bitwise operations. Sample files are `LFSR.encrypt` and `LFSR-decrypt.jpg` (the decrypted file happens to be a `.jpg`) for the initial fill $255 = 11111111_{2}$ and recursive function $$ a_{n} = a_{n-4} + a_{n-5} + a_{n-6} + a_{n-8} \pmod{2}. $$
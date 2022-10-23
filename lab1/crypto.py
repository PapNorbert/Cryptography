#!/usr/bin/env python3 -tt
"""
File: crypto.py
---------------
Assignment 1: Cryptography
Course: Kriptografia
Name: Pap Norbert-Raymond
pnim2069

"""


# Caesar Cipher
def encrypt_caesar(plaintext):
    """Encrypt plaintext using a Caesar cipher.
    """
    encryptedtext = ""
    AAscii = ord('A')
    ZAscii = ord('Z')
    differenceAscii = ZAscii - AAscii + 1
    for letter in plaintext:
        letterAscii = ord(letter)
        if AAscii <= letterAscii <= ZAscii:  # check if upperletter by ascii code
            if letterAscii + 3 > ZAscii:
                encryptedtext += chr(letterAscii + 3 - differenceAscii)
            else:
                encryptedtext += chr(letterAscii + 3)
        else:  # if letter is not uppercase
            encryptedtext += letter
    return encryptedtext


def decrypt_caesar(ciphertext):
    """Decrypt a ciphertext using a Caesar cipher.
    """
    decryptedtext = ""
    AAscii = ord('A')
    ZAscii = ord('Z')
    differenceAscii = ZAscii - AAscii + 1
    for letter in ciphertext:
        letterAscii = ord(letter)
        if AAscii <= letterAscii <= ZAscii:
            if letterAscii - 3 < AAscii:
                decryptedtext += (chr(letterAscii - 3 + differenceAscii))
            else:
                decryptedtext += (chr(letterAscii - 3))
        else:
            decryptedtext += letter
    return decryptedtext


def encrypt_caesar_ascii(plaintext):
    """Encrypt plaintext containing any ASCII caracters using a Caesar cipher.
    """
    encryptedtext = ""
    for character in plaintext:
        encryptedtext += chr((ord(character) + 3) % 256)

    return encryptedtext


def decrypt_caesar_ascii(ciphertext):
    """Decrypt a ciphertext containing any ASCII caracters using a Caesar cipher.
    """
    decryptedtext = ""
    for character in ciphertext:
        decryptedtext += chr((ord(character) - 3) % 256)
    return decryptedtext


# Vigenere Cipher

def encrypt_vigenere(plaintext, keyword):
    """Encrypt plaintext using a Vigenere cipher with a keyword.
    """
    if len(plaintext) < 1 or len(keyword) < 1:
        return 'Both parameters should have minimum length of 1!\nCould not encrypt'

    plaintext = plaintext.upper()
    keyword = keyword.upper()

    encryptedtext = ""
    AAscii = ord('A')
    ZAscii = ord('Z')
    for i in range(len(plaintext)):
        letterAscii = ord(plaintext[i])
        if AAscii <= letterAscii <= ZAscii:
            toAdd = ord(keyword[i % len(keyword)])
            encryptedtext += chr((letterAscii + toAdd) % 26 + AAscii)
        else:  # if letter is not uppercase
            encryptedtext += plaintext[i]
    return encryptedtext


def decrypt_vigenere(ciphertext, keyword):
    """Decrypt ciphertext using a Vigenere cipher with a keyword.
    """
    if len(ciphertext) < 1 or len(keyword) < 1:
        return 'Both parameters should have minimum length of 1!\nCould not decrypt'
    ciphertext = ciphertext.upper()
    keyword = keyword.upper()

    decryptedtext = ""
    AAscii = ord('A')
    ZAscii = ord('Z')
    for i in range(len(ciphertext)):
        letterAscii = ord(ciphertext[i])
        if AAscii <= letterAscii <= ZAscii:
            toSubstract = ord(keyword[i % len(keyword)])
            decryptedtext += chr((letterAscii - toSubstract) % 26 + AAscii)
        else:  # if letter is not uppercase
            decryptedtext += ciphertext[i]
    return decryptedtext


def encrypt_scytale(plaintext, circumference, binary=False):
    """Decrypt ciphertext using a Scytale cipher with a circumference(number).
    """
    try:
        circumference = int(circumference)
    except:
        return 'The second parameter(circumference) needs to be a number greater than 0!\n Could not encrypt'

    if circumference < 1:
        return 'The second parameter(circumference) needs to be a number greater than 0!\n Could not encrypt'
    if len(plaintext) < 1:
        return 'The text should have minimum length of 1!\nCould not encrypt'
    encryptedtext = []
    for i in range(circumference):
        encryptedtext.extend([plaintext[i::circumference]])
        # the circumference-th element starting from i
    if binary:
        return b''.join(encryptedtext)
    return "".join(encryptedtext)


def decrypt_scytale(ciphertext, circumference, binary=False):
    """Decrypt ciphertext using a Scytale cipher with a circumference(number).
    """
    if len(ciphertext) < 1:
        return 'The text should have minimum length of 1!\nCould not decrypt'
    try:
        circumference = int(circumference)
    except:
        return 'The second parameter(circumference) needs to be a number greater than 0!\n Could not encrypt'
    if circumference < 1:
        return 'The second parameter(circumference) needs to be a number greater than 0!\n Could not decrypt'

    decryptedtext = ""
    if binary:
        decryptedtext = bytearray(b'')

    newCircumference = len(ciphertext) // circumference
    fullColumns = circumference
    if (len(ciphertext) % circumference) != 0:
        newCircumference += 1
        fullColumns = (len(ciphertext) % circumference)
    differences = []
    for i in range(fullColumns):
        differences.append(0)
    for i in range(circumference - fullColumns):
        differences.append(i)
    # if the length cannot be divided with the circumference without remnants
    # it means during encryption there were not full rows
    # the remnants = nr of full rows, during decryption = nr of full columns, where
    # we need to shift which letter we take, thw last row will not be full

    for i in range(newCircumference):
        # i- number of rows
        columnRange = circumference
        if i == newCircumference - 1:
            columnRange = fullColumns
        for j in range(columnRange):
            # j- number of columns
            if binary:
                decryptedtext.append(ciphertext[i + j * newCircumference - differences[j]])
            else:
                decryptedtext += ciphertext[i + j * newCircumference - differences[j]]

    return decryptedtext


def encrypt_railfence(plaintext, num_rails):
    if len(plaintext) < 1:
        return 'The text should have minimum length of 1!\nCould not encrypt'
    try:
        num_rails = int(num_rails)
    except:
        return 'The second parameter(number of rails) needs to be a number greater than 0!\n Could not encrypt'
    if num_rails < 1:
        return 'The second parameter(number of rails) needs to be a number greater than 0!\n Could not encrypt'

    encryptedtext = ""
    rail = [['--' for _ in range(len(plaintext))]
            for _ in range(num_rails)]
    # creating the rail in a matrix
    down = True  # direction
    row = 0
    col = 0
    # put the letters on their place
    for letter in plaintext:
        rail[row][col] = letter
        col += 1
        if down:
            row += 1
        else:
            row -= 1
        if row == 0 or row == num_rails - 1:
            down = not down
    # read the text by each row
    for row in range(num_rails):
        for col in range(len(plaintext)):
            if rail[row][col] != '--':
                encryptedtext += rail[row][col]
    return encryptedtext


def decrypt_railfence(ciphertext, num_rails):
    if len(ciphertext) < 1:
        return 'The text should have minimum length of 1!\nCould not decrypt'
    try:
        num_rails = int(num_rails)
    except:
        return 'The second parameter(number of rails) needs to be a number greater than 0!\n Could not decrypt'
    if num_rails < 1:
        return 'The second parameter(number of rails) needs to be a number greater than 0!\n Could not decrypt'

    decryptedtext = ""
    rail = [['--' for _ in range(len(ciphertext))]
            for _ in range(num_rails)]
    down = True  # direction
    row = 0
    col = 0
    # mark the places where letters need to go
    for _letter in ciphertext:
        rail[row][col] = '-'
        col += 1
        if down:
            row += 1
        else:
            row -= 1
        if row == 0 or row == num_rails - 1:
            down = not down

    ind = 0
    # place the letter by each row
    for row in range(num_rails):
        for col in range(len(ciphertext)):
            if rail[row][col] != '--':
                rail[row][col] = ciphertext[ind]
                ind += 1

    # read the text by columns 
    down = True
    row = 0
    col = 0
    # mark the places where letters need to go
    while col < len(ciphertext):
        decryptedtext += rail[row][col]
        col += 1
        if down:
            row += 1
        else:
            row -= 1
        if row == 0 or row == num_rails - 1:
            down = not down

    return decryptedtext

#!/usr/bin/env python3 -tt
"""
File: crypto.py
---------------
Assignment 1: Cryptography
Course: Kriptografia
Name: Pap Norbert-Raymond
pnim2069

"""
import utils


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


# Vigenere Cipher

def encrypt_vigenere(plaintext, keyword):
    """Encrypt plaintext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    raise NotImplementedError  # Your implementation here


def decrypt_vigenere(ciphertext, keyword):
    """Decrypt ciphertext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    raise NotImplementedError  # Your implementation here

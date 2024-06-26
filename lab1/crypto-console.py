#!/usr/bin/env python3 -tt
"""
File: crypto-console.py
-----------------------
Implements a console menu to interact with the cryptography functions exported
by the crypto module.

If you are a student, you shouldn't need to change anything in this file.
"""
import random

from crypto import (encrypt_caesar, decrypt_caesar,
                    encrypt_vigenere, decrypt_vigenere,
                    encrypt_scytale, decrypt_scytale,
                    encrypt_railfence, decrypt_railfence,
                    encrypt_caesar_ascii, decrypt_caesar_ascii)


#############################
# GENERAL CONSOLE UTILITIES #
#############################

def get_tool():
    print("* Tool *")
    return _get_selection("(C)aesar, (A)scii Caesar,(V)igenere, (B)inary Scytale, (S)cytale or (R)ailfence? ", "CAVBSR")


def get_action():
    """Return true iff encrypt"""
    print("* Action *")
    return _get_selection("(E)ncrypt or (D)ecrypt? ", "ED")


def get_filename():
    filename = input("Filename? ")
    while not filename:
        filename = input("Filename? ")
    return filename


def get_input(binary=False):
    print("* Input *")
    choice = _get_selection("(F)ile or (S)tring? ", "FS")
    if choice == 'S':
        text = input("Enter a string: ").strip().upper()
        while not text:
            text = input("Enter a string: ").strip().upper()
        if binary:
            return bytes(text, encoding='utf8')
        return text
    else:
        filename = get_filename()
        flags = 'r'
        if binary:
            flags += 'b'
        with open(filename, flags) as infile:
            return infile.read()


def set_output(output, binary=False):
    print("* Output *")
    choice = _get_selection("(F)ile or (S)tring? ", "FS")
    if choice == 'S':
        print(output)
    else:
        filename = get_filename()
        flags = 'w'
        if binary:
            flags += 'b'
            with open(filename, flags) as outfile:
                print("Writing data to {}...".format(filename))
                outfile.write(output)
        else:
            with open(filename, flags, encoding="utf-8") as outfile:
                print("Writing data to {}...".format(filename))
                outfile.write(output)


def _get_selection(prompt, options):
    choice = input(prompt).upper()
    while not choice or choice[0] not in options:
        choice = input("Please enter one of {}. {}".format('/'.join(options), prompt)).upper()
    return choice[0]


def get_yes_or_no(prompt, reprompt=None):
    """
    Asks the user whether they would like to continue.
    Responses that begin with a `Y` return True. (case-insensitively)
    Responses that begin with a `N` return False. (case-insensitively)
    All other responses (including '') cause a reprompt.
    """
    if not reprompt:
        reprompt = prompt

    choice = input("{} (Y/N) ".format(prompt)).upper()
    while not choice or choice[0] not in ['Y', 'N']:
        choice = input("Please enter either 'Y' or 'N'. {} (Y/N)? ".format(reprompt)).upper()
    return choice[0] == 'Y'


def clean_caesar(text):
    """Convert text to a form compatible with the preconditions imposed by Caesar cipher"""
    return text.upper()


def clean_vigenere(text):
    return ''.join(ch for ch in text.upper() if ch.isupper())


def run_caesar():
    action = get_action()
    encrypting = action == 'E'
    data = clean_caesar(get_input(binary=False))

    print("* Transform *")
    print("{}crypting {} using Caesar cipher...".format('En' if encrypting else 'De', data))

    output = (encrypt_caesar if encrypting else decrypt_caesar)(data)

    set_output(output)


def run_vigenere():
    action = get_action()
    encrypting = action == 'E'
    data = clean_vigenere(get_input(binary=False))

    print("* Transform *")
    keyword = clean_vigenere(input("Keyword? "))

    print("{}crypting {} using Vigenere cipher and keyword {}...".format('En' if encrypting else 'De', data, keyword))

    output = (encrypt_vigenere if encrypting else decrypt_vigenere)(data, keyword)

    set_output(output)


def run_scytale():
    action = get_action()
    encrypting = action == 'E'
    data = get_input(binary=False)

    print("* Transform *")
    circumference = input("Circumference? (number) ")

    print("{}crypting {} using Scytale cipher and circumference {}...".format('En' if encrypting else 'De', data,
                                                                              circumference))

    output = (encrypt_scytale if encrypting else decrypt_scytale)(data, circumference)

    set_output(output)


def run_railfence():
    action = get_action()
    encrypting = action == 'E'
    data = get_input(binary=False)

    print("* Transform *")
    num_rails = input("Number of rails? ")

    print("{}crypting {} using Railfence cipher and number of rails: {} ...".format('En' if encrypting else 'De', data,
                                                                                    num_rails))

    output = (encrypt_railfence if encrypting else decrypt_railfence)(data, num_rails)

    set_output(output)


def run_caesar_ascii():
    action = get_action()
    encrypting = action == 'E'
    data = get_input(binary=False)

    print("* Transform *")
    print("{}crypting {} using ASCII Caesar cipher ...".format('En' if encrypting else 'De', data))

    output = (encrypt_caesar_ascii if encrypting else decrypt_caesar_ascii)(data)

    set_output(output)


def run_scytale_binary():
    action = get_action()
    encrypting = action == 'E'
    data = get_input(binary=True)

    print("* Transform *")
    circumference = input("Circumference? (number) ")

    print("{}crypting  using Scytale cipher for binary file with circumference: {} ...".format(
        'En' if encrypting else 'De', circumference))

    output = (encrypt_scytale if encrypting else decrypt_scytale)(data, circumference, True)

    set_output(output, binary=True)


def run_suite():
    """
    Runs a single iteration of the cryptography suite.

    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.
    """
    print('-' * 34)
    tool = get_tool()
    # This isn't the cleanest way to implement functional control flow,
    # but I thought it was too cool to not sneak in here!
    commands = {
        'C': run_caesar,  # Caesar Cipher
        'A': run_caesar_ascii,
        'V': run_vigenere,  # Vigenere Cipher
        'S': run_scytale,  # Scytale Cipher
        'R': run_railfence,  # Railfence Cipher
        'B': run_scytale_binary,
    }
    commands[tool]()


def main():
    print("Welcome to the Cryptography Suite!")
    run_suite()
    while get_yes_or_no("Again?"):
        run_suite()
    print("Goodbye!")


if __name__ == '__main__':
    main()

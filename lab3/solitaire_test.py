from solitaire import checkSolitaireKey, generate_half_solitaire_key, generate_second_half_solitaire_key, \
    solitaireRandomNumber, en_decrypt_solitaire
from random import randint


def test_solitaire_key_generation():
    key = generate_half_solitaire_key()
    generate_second_half_solitaire_key(key)
    assert checkSolitaireKey(key)


def test_solitaire_random_number():
    key = generate_half_solitaire_key()
    generate_second_half_solitaire_key(key)
    rand = solitaireRandomNumber(key)
    for i in range(25):
        assert 0 <= rand <= 255


def test_solitaire_encryption():
    key = generate_half_solitaire_key()
    generate_second_half_solitaire_key(key)
    keyCopy = key.copy()
    message = 'This is a test message343 % . l'
    for i in range(50):
        message += chr(randint(32, 240))
    encrypted, _newKey = en_decrypt_solitaire(message, key)
    decrypted, _newKey = en_decrypt_solitaire(encrypted, keyCopy)
    # decryption is done with the same key as encryption
    assert decrypted == message

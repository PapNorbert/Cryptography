from random import randint


# returns a random number between 0-255
def solitaireRandomNumber(key):
    # card numbering:
    #  1, 2,...,13 are A,2,...,K of clubs
    # 14,15,...,26 are A,2,...,K of diamonds
    # 27,28,...,39 are A,2,...,K of hearts
    # 40,41,...,52 are A,2,...,K of spades
    # 53 white joker, 54 black joker
    secondkey = generateNewKey(key)

    moveWJoker1Down(key)
    moveWJoker1Down(secondkey)
    moveBJoker2Down(key)
    moveBJoker2Down(secondkey)
    edgesSwap(key)
    edgesSwap(secondkey)
    cutFromNWithoutLast(key, key[-1])
    cutFromNWithoutLast(secondkey, secondkey[-1])

    value1 = key[key[0] % 54]  # if first card is black joker, value is 54, means the first element of key (cyclic)
    value2 = secondkey[secondkey[0] % 54]

    return (value1 * value2) % 255


# generate a new key based on a given one
def generateNewKey(key):
    newKey = key.copy()
    # swaps
    newKey[3], newKey[30] = newKey[30], newKey[3]
    newKey[9], newKey[12] = newKey[12], newKey[9]
    newKey[51], newKey[4] = newKey[4], newKey[51]
    newKey[7], newKey[36] = newKey[36], newKey[7]
    newKey[22], newKey[21] = newKey[21], newKey[22]
    newKey[8], newKey[44] = newKey[44], newKey[8]
    return newKey


# swap cards before first joker with those after second joker
def edgesSwap(key):
    # 53 white joker, 54 black joker
    firstJi, secondJi = key.index(53), key.index(54)
    if firstJi > secondJi:
        firstJi, secondJi = secondJi, firstJi
    key[:] = key[secondJi + 1:] + key[firstJi:secondJi + 1] + key[:firstJi]


# move black joker 2 down
def moveBJoker2Down(key):
    n = key.index(54)
    if n < 52:
        key[n], key[n + 1], key[n + 2] = key[n + 1], key[n + 2], key[n]
    elif n == 52:  # before last car
        key[1:] = key[n:n + 1] + key[1:n] + key[-1:]
    else:  # last card
        key[1:] = key[1:2] + key[-1:] + key[2:-1]


# move white joker 1 up
def moveWJoker1Down(key):
    n = key.index(53)
    if n < 53:
        key[n], key[n + 1] = key[n + 1], key[n]
    else:  # last card
        key[1:] = key[-1:] + key[1:-1]


# cut after the n-th card, leaving the bottom card in place.
def cutFromNWithoutLast(key, n):
    if n == 54:
        n = 53  # value of black joker is 54, we need to leave that card in place if it's last
    key[:-1] = key[n:-1] + key[:n]


def checkSolitaireKey(key):
    i = 1
    while i <= 54:
        if key.count(i) == 1:
            i += 1
        else:
            return False
    return True


def generate_half_solitaire_key():
    key = []
    nrAdded = 0
    while nrAdded < 27:
        randNumber = randint(1, 54)
        if randNumber not in key:
            key.append(randNumber)
            nrAdded += 1
    return key


def generate_second_half_solitaire_key(key):
    allKeyValues = [x for x in range(1, 55)]
    for value in key:
        allKeyValues.remove(value)
    while len(key) != 54:
        randNumber = randint(0, len(allKeyValues) - 1)
        newValue = allKeyValues.pop(randNumber)
        key.append(newValue)


def en_decrypt_solitaire(text, key):
    newText = ''
    for simbol in text:
        randValue = solitaireRandomNumber(key)
        newCharacter = chr(ord(simbol) ^ randValue)
        newText += newCharacter
    return newText, key


def encrypt(text, outFile):
    # key: [A-Za-z01]
    key = getKey("be.txt")
    processedKey = processKey(key)
    if not processedKey:
        print("Wrong key format")
    else:
        out = open(outFile, "w", encoding='latin-1')
        for simbol in text:
            randValue = solitaireRandomNumber(processedKey)
            if simbol == "\n":
                out.write(simbol)
            else:
                newCharacter = chr(ord(simbol) ^ randValue)
                out.write(newCharacter)
        out.close()


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


# cut after the n-th card, leaving the bottom card in place.
def cutFromNWithoutLast(key, n):
    if n == 54:
        n = 53  # value of black joker is 54, we need to leave that card in place if it's last
    key[:-1] = key[n:-1] + key[:n]


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


# process the key based on the solitaire requirements
def processKey(key):
    if len(key) != 54:
        return []
    # a->1, ...  z->26
    # A->27, ... Z->52
    # 0->53, 1->54
    processedKey = []
    for character in key:
        if character.isalpha():
            if character.islower():
                value = ord(character) - ord("a") + 1
                if value not in processedKey:
                    processedKey.append(value)
                else:
                    return []
            else:
                value = ord(character) - ord("A") + 1 + 26
                if value not in processedKey:
                    processedKey.append(value)
                else:
                    return []
        elif character == "0":
            if 53 not in processedKey:
                processedKey.append(53)
            else:
                return []
        elif character == "1":
            if 54 not in processedKey:
                processedKey.append(54)
            else:
                return []
        else:
            # not a correct character
            return []
    return processedKey


def getKey(filename):
    inFile = open(filename, 'r')
    key = inFile.readline()
    inFile.close()
    return key


def getText(filename):
    inFile = open(filename, 'r', encoding='latin-1')
    text = inFile.read()
    inFile.close()
    return text


def main():
    text = getText("szoveg.txt")
    encrypt(text, "crypted.txt")

    text = getText("crypted.txt")
    encrypt(text, "decrypted.txt")


if __name__ == '__main__':
    main()

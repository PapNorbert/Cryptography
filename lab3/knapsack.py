from random import randint

from utils import coprime, modinv, byte_to_bits, bits_to_byte


def generate_private_key_knapsack(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem.
    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:
    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)
    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    total = randint(1, 5)
    w = [total]
    for i in range(1, n):  # first is already generated
        w.append(randint(total + 1, 2 * total))
        total += w[i]
    q = randint(total + 1, 2 * total)
    got_r = False
    r = 2
    while not got_r and r < q:
        if coprime(q, r):
            got_r = True
        else:
            r += 1
    return w, q, r


def create_public_key_knapsack(private_key):
    """Create a public key corresponding to the given private key.
    To accomplish this, you only need to build and return `beta` as described in the handout.
        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q
    Hint: this can be written in one line using a list comprehension
    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    @return n-tuple public key
    """
    return [(w_i * private_key[2]) % private_key[1] for w_i in private_key[0]]


def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.
    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message
    @param message The message to be encrypted
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints
    @return list of ints representing encrypted bytes
    """
    encrypted = []
    for letter in message:
        bits = byte_to_bits(ord(letter))
        c = 0
        for a_i, b_i in zip(bits, public_key):
            c += a_i * b_i
        encrypted.append(c)
    return encrypted


def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key
    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back
    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r
    @return bytearray or str of decrypted characters
    """
    decrypted = ''
    s = modinv(private_key[2], private_key[1])
    for c in message:
        c2 = (c * s) % private_key[1]
        bits = []
        for w_i in reversed(private_key[0]):
            if w_i > c2:
                bits.append(0)
            else:
                bits.append(1)
                c2 -= w_i
        bits.reverse()
        decrypted += chr(bits_to_byte(bits))  # transform the bits back to ascii characters
    return decrypted

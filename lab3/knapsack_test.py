from knapsack import generate_private_key_knapsack, create_public_key_knapsack, encrypt_mh, decrypt_mh
from utils import is_superincreasing


def test_private_key_w_seperincreasing():
    private_key = generate_private_key_knapsack()
    assert is_superincreasing(private_key[0])


def test_mh_decryption():
    private_key = generate_private_key_knapsack()
    public_key = create_public_key_knapsack(private_key)
    encrypted = encrypt_mh('This is a test message343 % . l', public_key)
    decrypted = decrypt_mh(encrypted, private_key)
    assert 'This is a test message343 % . l' == decrypted

def test_mh_decryption2():
    private_key = generate_private_key_knapsack()
    public_key = create_public_key_knapsack(private_key)
    message = '''Section 1.10.32 of "de Finibus Bonorum et Malorum", written by Cicero in 45 BC
"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur 123243256}{\*magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur?'''
    encrypted = encrypt_mh(message, public_key)
    decrypted = decrypt_mh(encrypted, private_key)
    assert message == decrypted
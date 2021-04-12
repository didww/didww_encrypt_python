from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad
from Cryptodome.Signature import pss


def encrypt_rsa_oaep(data: bytes, pubkey: str) -> bytes:
    key = RSA.import_key(pubkey)
    cipher_rsa = PKCS1_OAEP.new(
        key=key, hashAlgo=SHA256, mgfunc=lambda x, y: pss.MGF1(x, y, SHA256)
    )
    return cipher_rsa.encrypt(data)


def encrypt(data: bytes, pubkey_a: str, pubkey_b: str) -> bytes:
    """Encrypt data with public keys

    :param data: data that you want to encrypt
    :param pubkey_a: first RSA public key
    :param pubkey_b:  second RSA public key
    :return: encrypted data
    """
    aes_key = get_random_bytes(32)  # AES 256
    aes_iv = get_random_bytes(AES.block_size)
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    encrypted_aes = cipher.encrypt(pad(data, AES.block_size))
    aes_key_iv = aes_key + aes_iv
    encrypted_aes_key_iv_a = encrypt_rsa_oaep(aes_key_iv, pubkey_a)
    encrypted_aes_key_iv_b = encrypt_rsa_oaep(aes_key_iv, pubkey_b)
    return encrypted_aes_key_iv_a + encrypted_aes_key_iv_b + encrypted_aes

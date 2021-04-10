import os
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Hash import SHA256
from Cryptodome.Util.Padding import unpad
from Cryptodome.Signature import pss


def decrypt(data: bytes, private_key: str, key_index: int):
    key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(
        key=key, hashAlgo=SHA256, mgfunc=lambda x, y: pss.MGF1(x, y, SHA256)
    )
    encrypted_aes_key_iv = (
        data[0:512] if key_index == 0 else data[512:1024]
    )  # RSA 4096 OAEP encrypts to 512 bytes
    aes_key_iv = cipher_rsa.decrypt(
        encrypted_aes_key_iv
    )  # 32 bytes aes_key + 16 bytes aes_iv
    cipher_aes = AES.new(aes_key_iv[0:32], AES.MODE_CBC, aes_key_iv[32:])
    return unpad(cipher_aes.decrypt(data[1024:]), AES.block_size)


def read_fixture(path: str):
    tests_root = os.path.dirname(__file__)
    with open(f"{tests_root}/fixtures/{path}", mode="r", encoding="utf-8") as f:
        return f.read()


def generate_rsa_key():
    rsa = RSA.generate(4096)
    pubkey = rsa.public_key().export_key("PEM")
    private_key = rsa.export_key("PEM")
    return pubkey, private_key

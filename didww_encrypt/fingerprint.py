from base64 import b64decode
from Cryptodome.Hash import SHA1

SEPARATOR = ':::'


def pubkey_pem_to_bin(pubkey: str) -> bytes:
    pubkey = pubkey.replace(r"\r\n", r"\n")
    if pubkey[:-1] != "\n":
        pubkey += "\n"
    pem = "".join(pubkey.split("\n")[1:-2])
    return b64decode(pem.encode('ascii'))


def fingerprint_for(pubkey: bytes) -> bytes:
    digest = SHA1.new()
    digest.update(pubkey)
    return digest.digest()


def calculate_fingerprint(pubkey_a: str, pubkey_b: str) -> str:
    fingerprint_a = fingerprint_for(pubkey_pem_to_bin(pubkey_a)).hex()
    fingerprint_b = fingerprint_for(pubkey_pem_to_bin(pubkey_b)).hex()
    return "".join([fingerprint_a, SEPARATOR, fingerprint_b])

from base64 import b64decode
from Cryptodome.Hash import SHA1

SEPARATOR = ":::"


def pubkey_pem_to_bin(pubkey: str) -> bytes:
    key = pubkey.replace(r"\r\n", r"\n")
    if key[-1:] != "\n":
        key += "\n"
    pem = "".join(key.split("\n")[1:-2])
    return b64decode(pem.encode("ascii"))


def fingerprint_for(pubkey: bytes) -> str:
    digest = SHA1.new(pubkey)
    return digest.hexdigest()


def calculate_fingerprint(pubkey_a: str, pubkey_b: str) -> str:
    fingerprint_a = fingerprint_for(pubkey_pem_to_bin(pubkey_a))
    fingerprint_b = fingerprint_for(pubkey_pem_to_bin(pubkey_b))
    return "".join([fingerprint_a, SEPARATOR, fingerprint_b])

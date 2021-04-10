from didww_encrypt.fingerprint import calculate_fingerprint
from didww_encrypt.encryption import encrypt
from didww_encrypt.fetching import fetch_public_keys
from . import MODE_SANDBOX, MODE_PRODUCTION, URI_SANDBOX, URI_PRODUCTION


class DIDWW_Encrypt:
    def __init__(self, pubkey_a: str, pubkey_b: str):
        self.pubkey_a = pubkey_a
        self.pubkey_b = pubkey_b
        self.fingerprint = calculate_fingerprint(self.pubkey_a, self.pubkey_b)

    def encrypt(self, data_bytes: bytes) -> bytes:
        return encrypt(data_bytes, self.pubkey_a, self.pubkey_b)


def new(mode: str = None, uri: str = None) -> DIDWW_Encrypt:
    if uri is not None:
        pubkey_a, pubkey_b = fetch_public_keys(uri)
    elif mode == MODE_SANDBOX:
        pubkey_a, pubkey_b = fetch_public_keys(URI_SANDBOX)
    elif mode == MODE_PRODUCTION:
        pubkey_a, pubkey_b = fetch_public_keys(URI_PRODUCTION)
    else:
        raise ValueError("Valid mode, or uri must be provided")

    return DIDWW_Encrypt(pubkey_a, pubkey_b)

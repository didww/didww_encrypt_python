from didww_encrypt.fingerprint import calculate_fingerprint
from didww_encrypt.encryption import encrypt
from didww_encrypt.fetching import fetch_public_keys

MODE_SANDBOX = "sandbox"
MODE_PRODUCTION = "production"
URI_SANDBOX = "https://sandbox-api.didww.com/v3/public_keys"
URI_PRODUCTION = "https://api.didww.com/v3/public_keys"
MODES = [MODE_SANDBOX, MODE_PRODUCTION]


class DIDWW_Encrypt:
    def __init__(self, mode: str = None, uri: str = None):
        if uri is not None:
            self.pubkey_a, self.pubkey_b = fetch_public_keys(uri)
        elif mode == MODE_SANDBOX:
            self.pubkey_a, self.pubkey_b = fetch_public_keys(URI_SANDBOX)
        elif mode == MODE_PRODUCTION:
            self.pubkey_a, self.pubkey_b = fetch_public_keys(URI_PRODUCTION)
        else:
            raise ValueError("Valid mode, or uri must be provided")
        self.fingerprint = calculate_fingerprint(self.pubkey_a, self.pubkey_b)

    def encrypt(self, data_bytes: bytes) -> bytes:
        return encrypt(data_bytes, self.pubkey_a, self.pubkey_b)


def new(mode: str = None, uri: str = None) -> DIDWW_Encrypt:
    return DIDWW_Encrypt(mode, uri)

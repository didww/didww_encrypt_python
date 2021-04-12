"""
This is Python 3 module and utility to encrypt file for DIDWW API 3.

File encrypted with mode `sandbox` could be uploaded to `POST https://sandbox-api.didww.com/v3/encrypted_files`.

File encrypted with mode `production` could be uploaded to `POST https://api.didww.com/v3/encrypted_files`.

    .. highlight:: python
    .. code-block:: python

        from didww_encrypt import Encrypt, MODE_PRODUCTION

        with open("doc.pdf", mode="rb") as f:
            data = f.read()

        enc = Encrypt.new(MODE_PRODUCTION)
        enc_data = enc.encrypt(data)
        enc_filename = "doc.pdf.enc"
        with open(enc_filename, mode="wb") as f:
            f.write(enc_data)

        print(f"encrypted file saved: {enc_filename}")
        print(f"fingerprint: {enc.fingerprint}")
"""

MODE_SANDBOX = "sandbox"
MODE_PRODUCTION = "production"
URI_SANDBOX = "https://sandbox-api.didww.com/v3/public_keys"
URI_PRODUCTION = "https://api.didww.com/v3/public_keys"
MODES = [MODE_SANDBOX, MODE_PRODUCTION]

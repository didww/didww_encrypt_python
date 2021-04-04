import unittest
from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Hash import SHA256
from Cryptodome.Util.Padding import unpad
from Cryptodome.Signature import pss
from didww_encrypt import encryption


def decrypt(data: bytes, rsa, first_key: bool):
    cipher_rsa = PKCS1_OAEP.new(key=rsa, hashAlgo=SHA256, mgfunc=lambda x, y: pss.MGF1(x, y, SHA256))
    encrypted_aes_key = data[0:512] if first_key else data[512:1024]  # rsa 4096 encrypts to 512 bytes
    aes_key = cipher_rsa.decrypt(encrypted_aes_key)
    aes_iv = data[1024:1040]  # 2 * 512 bytes + 16 bytes (aes_iv)
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    return unpad(cipher_aes.decrypt(data[1040:]), AES.block_size)


class TestEncryption(unittest.TestCase):

    def test_encrypt(self):
        rsa_a = RSA.generate(4096)
        rsa_b = RSA.generate(4096)
        pubkey_a = rsa_a.public_key().export_key('PEM')
        pubkey_b = rsa_b.public_key().export_key('PEM')
        data = get_random_bytes(1024 * 1024)  # 1MB
        encrypted = encryption.encrypt(data, pubkey_a, pubkey_b)
        decrypted_a = decrypt(encrypted, rsa_a, True)
        decrypted_b = decrypt(encrypted, rsa_b, False)
        self.assertEqual(decrypted_a, data)
        self.assertEqual(decrypted_b, data)


if __name__ == '__main__':
    unittest.main()

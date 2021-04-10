import unittest
from tests import decrypt, generate_rsa_key
from Cryptodome.Random import get_random_bytes
from didww_encrypt import encryption


class TestEncryption(unittest.TestCase):
    def test_encrypt(self):
        pubkey_a, private_key_a = generate_rsa_key()
        pubkey_b, private_key_b = generate_rsa_key()
        data = get_random_bytes(1024 * 1024 * 20)  # 20MB
        encrypted = encryption.encrypt(data, pubkey_a, pubkey_b)
        decrypted_a = decrypt(encrypted, private_key_a, 0)
        decrypted_b = decrypt(encrypted, private_key_b, 1)
        self.assertEqual(data, decrypted_a)
        self.assertEqual(data, decrypted_b)

import json
import unittest
import httpretty
from tests import decrypt, read_fixture
from Cryptodome.Random import get_random_bytes
from didww_encrypt import (
    Encrypt,
    URI_SANDBOX,
    URI_PRODUCTION,
    MODE_SANDBOX,
    MODE_PRODUCTION,
)


class TestEncrypt(unittest.TestCase):
    @httpretty.activate(allow_net_connect=False)
    def test_initialize_mode_sandbox(self):
        httpretty.register_uri(
            httpretty.GET, URI_SANDBOX, body=read_fixture("public_keys.json")
        )
        enc = Encrypt.new(mode=MODE_SANDBOX)
        self.assertEqual(
            "ca5af2d14bee923a0a0d1687b7c77e7211a57f84:::683150ee69b4d906aa883d0ac12b0fdd79f95bcf",
            enc.fingerprint,
        )
        data = get_random_bytes(1024 * 1024)  # 1MB
        encrypted = enc.encrypt(data)
        private_keys = json.loads(read_fixture("private_keys.json"))
        decrypted_a = decrypt(encrypted, private_keys["private_key_a"], 0)
        self.assertEqual(data, decrypted_a)
        decrypted_b = decrypt(encrypted, private_keys["private_key_b"], 1)
        self.assertEqual(data, decrypted_b)

    @httpretty.activate(allow_net_connect=False)
    def test_initialize_mode_production(self):
        httpretty.register_uri(
            httpretty.GET, URI_PRODUCTION, body=read_fixture("public_keys.json")
        )
        enc = Encrypt.new(mode=MODE_PRODUCTION)
        self.assertEqual(
            "ca5af2d14bee923a0a0d1687b7c77e7211a57f84:::683150ee69b4d906aa883d0ac12b0fdd79f95bcf",
            enc.fingerprint,
        )
        data = get_random_bytes(1024 * 1024)  # 1MB
        encrypted = enc.encrypt(data)
        private_keys = json.loads(read_fixture("private_keys.json"))
        decrypted_a = decrypt(encrypted, private_keys["private_key_a"], 0)
        self.assertEqual(data, decrypted_a)
        decrypted_b = decrypt(encrypted, private_keys["private_key_b"], 1)
        self.assertEqual(data, decrypted_b)

    @httpretty.activate(allow_net_connect=False)
    def test_initialize_custom_uri(self):
        uri = "https://api.example.com/keys"
        httpretty.register_uri(
            httpretty.GET, uri, body=read_fixture("public_keys.json")
        )
        enc = Encrypt.new(uri=uri)
        self.assertEqual(
            "ca5af2d14bee923a0a0d1687b7c77e7211a57f84:::683150ee69b4d906aa883d0ac12b0fdd79f95bcf",
            enc.fingerprint,
        )
        data = get_random_bytes(1024 * 1024)  # 1MB
        encrypted = enc.encrypt(data)
        private_keys = json.loads(read_fixture("private_keys.json"))
        decrypted_a = decrypt(encrypted, private_keys["private_key_a"], 0)
        self.assertEqual(data, decrypted_a)
        decrypted_b = decrypt(encrypted, private_keys["private_key_b"], 1)
        self.assertEqual(data, decrypted_b)

    def test_without_mode_nor_uri(self):
        exception = None
        try:
            Encrypt.new()
        except BaseException as e:
            exception = e
        self.assertIsInstance(exception, ValueError)
        self.assertEqual("Valid mode, or uri must be provided", str(exception))

    def test_without_invalid_mode(self):
        exception = None
        try:
            Encrypt.new(mode="foo")
        except BaseException as e:
            exception = e
        self.assertIsInstance(exception, ValueError)
        self.assertEqual("Valid mode, or uri must be provided", str(exception))

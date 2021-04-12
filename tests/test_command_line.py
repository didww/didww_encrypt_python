import unittest
import json
import httpretty
import os
from tests import redirect_all, build_buffers, read_fixture, decrypt, TESTS_ROOT
from didww_encrypt import URI_SANDBOX, URI_PRODUCTION
from didww_encrypt.command_line import main


def run_main(args: list = None, in_data: bytes = None) -> (int, bytes, str):
    """Runs main command line and catch stdin, stdout, stderr.

    :param args: arguments for command line.
    :param in_data: stdin bytes.
    :return: exit code, stdout bytes, stderr string.
    """
    in_io, out_io, err_io = build_buffers(in_data is None)
    if in_data is not None:
        in_io.buffer.write(in_data)
    with redirect_all(in_io, out_io, err_io):
        exitcode = main(args=args)
    out_data = out_io.buffer.read()
    err_data = err_io.read()
    return exitcode, out_data, err_data


class TestCommandLine(unittest.TestCase):
    @httpretty.activate(allow_net_connect=False)
    def test_mode_sandbox(self):
        private_keys = json.loads(read_fixture("private_keys.json"))
        httpretty.register_uri(
            httpretty.GET, URI_SANDBOX, body=read_fixture("public_keys.json")
        )

        args = "--mode sandbox".split(" ")
        input_data = "test data".encode("utf-8")
        exitcode, out_data, err_data = run_main(args=args, in_data=input_data)

        self.assertEqual("", err_data)
        self.assertEqual(0, exitcode)

        decrypted_a = decrypt(out_data, private_keys["private_key_a"], 0)
        self.assertEqual(input_data, decrypted_a)
        decrypted_b = decrypt(out_data, private_keys["private_key_b"], 1)
        self.assertEqual(input_data, decrypted_b)

    @httpretty.activate(allow_net_connect=False)
    def test_mode_production(self):
        private_keys = json.loads(read_fixture("private_keys.json"))
        httpretty.register_uri(
            httpretty.GET, URI_PRODUCTION, body=read_fixture("public_keys.json")
        )

        args = "--mode production".split(" ")
        input_data = "test data".encode("utf-8")
        exitcode, out_data, err_data = run_main(args=args, in_data=input_data)

        self.assertEqual("", err_data)
        self.assertEqual(0, exitcode)

        decrypted_a = decrypt(out_data, private_keys["private_key_a"], 0)
        self.assertEqual(input_data, decrypted_a)
        decrypted_b = decrypt(out_data, private_keys["private_key_b"], 1)
        self.assertEqual(input_data, decrypted_b)

    @httpretty.activate(allow_net_connect=False)
    def test_input_file(self):
        private_keys = json.loads(read_fixture("private_keys.json"))
        httpretty.register_uri(
            httpretty.GET, URI_PRODUCTION, body=read_fixture("public_keys.json")
        )

        in_path = f"{TESTS_ROOT}/fixtures/test_file.txt"
        with open(in_path, mode="rb") as f:
            in_file_data = f.read()
        args = f"--mode production --input {in_path}".split(" ")
        exitcode, out_data, err_data = run_main(args=args)

        self.assertEqual("", err_data)
        self.assertEqual(0, exitcode)

        decrypted_a = decrypt(out_data, private_keys["private_key_a"], 0)
        self.assertEqual(in_file_data, decrypted_a)
        decrypted_b = decrypt(out_data, private_keys["private_key_b"], 1)
        self.assertEqual(in_file_data, decrypted_b)

    @httpretty.activate(allow_net_connect=False)
    def test_output_file(self):
        private_keys = json.loads(read_fixture("private_keys.json"))
        httpretty.register_uri(
            httpretty.GET, URI_PRODUCTION, body=read_fixture("public_keys.json")
        )

        input_data = "test data".encode("utf-8")
        out_path = f"{TESTS_ROOT}/fixtures/test.enc"
        args = f"--mode production --output {out_path}".split(" ")
        exitcode, out_data, err_data = run_main(args=args, in_data=input_data)
        with open(out_path, mode="rb") as f:
            out_file_data = f.read()
        os.remove(out_path)

        self.assertEqual("", err_data)
        self.assertEqual(0, exitcode)
        self.assertEqual(b"", out_data)

        decrypted_a = decrypt(out_file_data, private_keys["private_key_a"], 0)
        self.assertEqual(input_data, decrypted_a)
        decrypted_b = decrypt(out_file_data, private_keys["private_key_b"], 1)
        self.assertEqual(input_data, decrypted_b)

    @httpretty.activate(allow_net_connect=False)
    def test_fingerprint(self):
        httpretty.register_uri(
            httpretty.GET, URI_PRODUCTION, body=read_fixture("public_keys.json")
        )

        args = "--mode production -f".split(" ")
        exitcode, out_data, err_data = run_main(args=args)

        self.assertEqual("", err_data)
        self.assertEqual(0, exitcode)
        self.assertEqual(
            "ca5af2d14bee923a0a0d1687b7c77e7211a57f84:::683150ee69b4d906aa883d0ac12b0fdd79f95bcf\n",
            out_data.decode("utf-8"),
        )

    @httpretty.activate(allow_net_connect=False)
    def test_no_input(self):
        httpretty.register_uri(
            httpretty.GET, URI_PRODUCTION, body=read_fixture("public_keys.json")
        )

        args = "--mode production".split(" ")
        exitcode, out_data, err_data = run_main(args=args)

        self.assertEqual("input file or pipe data must be provided\n", err_data)
        self.assertEqual(2, exitcode)
        self.assertEqual(b"", out_data)

    @httpretty.activate(allow_net_connect=False)
    def test_fetch_failed(self):
        httpretty.register_uri(
            httpretty.GET,
            URI_PRODUCTION,
            status=500,
            body=json.dumps({"error": "server error"}),
        )

        args = "--mode production".split(" ")
        input_data = "test data".encode("utf-8")
        exitcode, out_data, err_data = run_main(args=args, in_data=input_data)

        self.assertEqual(
            f"failed to fetch keys from {URI_PRODUCTION}: 500 Internal Server Error\n",
            err_data,
        )
        self.assertEqual(3, exitcode)
        self.assertEqual(b"", out_data)

    @httpretty.activate(allow_net_connect=False)
    def test_custom_uri(self):
        uri = "https://example.com/keys"
        private_keys = json.loads(read_fixture("private_keys.json"))
        httpretty.register_uri(
            httpretty.GET, uri, body=read_fixture("public_keys.json")
        )

        args = f"--uri {uri}".split(" ")
        input_data = "test data".encode("utf-8")
        exitcode, out_data, err_data = run_main(args=args, in_data=input_data)

        self.assertEqual("", err_data)
        self.assertEqual(0, exitcode)

        decrypted_a = decrypt(out_data, private_keys["private_key_a"], 0)
        self.assertEqual(input_data, decrypted_a)
        decrypted_b = decrypt(out_data, private_keys["private_key_b"], 1)
        self.assertEqual(input_data, decrypted_b)

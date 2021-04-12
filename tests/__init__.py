import os
import contextlib
import sys
import io
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Hash import SHA256
from Cryptodome.Util.Padding import unpad
from Cryptodome.Signature import pss

TESTS_ROOT = os.path.dirname(__file__)


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
    with open(f"{TESTS_ROOT}/fixtures/{path}", mode="r", encoding="utf-8") as f:
        return f.read()


def generate_rsa_key():
    rsa = RSA.generate(4096)
    pubkey = rsa.public_key().export_key("PEM")
    private_key = rsa.export_key("PEM")
    return pubkey, private_key


class redirect_stdin(contextlib.AbstractContextManager):
    def __init__(self, new_target):
        self._new_target = new_target
        # We use a list of old targets to make this CM re-entrant
        self._old_targets = []

    def __enter__(self):
        self._old_targets.append(getattr(sys, "stdin"))
        setattr(sys, "stdin", self._new_target)
        return self._new_target

    def __exit__(self, exctype, excinst, exctb):
        setattr(sys, "stdin", self._old_targets.pop())


class redirect_all(contextlib.AbstractContextManager):
    """Wraps all input/output with buffers

    Inspired by contextlib.redirect_stdout, contextlib.redirect_stderr
    """

    def __init__(
        self,
        new_stdin: io.TextIOWrapper,
        new_stdout: io.TextIOWrapper,
        new_stderr: io.TextIOWrapper,
    ):
        self._new_stdin = new_stdin
        self._new_stdout = new_stdout
        self._new_stderr = new_stderr
        # We use a list of old targets to make this CM re-entrant
        self._old_targets = []

    def __enter__(self) -> (io.TextIOWrapper, io.TextIOWrapper, io.TextIOWrapper):
        self._old_targets.append(
            [
                getattr(sys, "stdin"),
                getattr(sys, "stdout"),
                getattr(sys, "stderr"),
            ]
        )
        setattr(sys, "stdin", self._new_stdin)
        setattr(sys, "stdout", self._new_stdout)
        setattr(sys, "stderr", self._new_stderr)
        self._new_stdin.seek(0)
        return self._new_stdin, self._new_stdout, self._new_stderr

    def __exit__(self, exctype, excinst, exctb):
        sys.stdout.seek(0)
        sys.stderr.seek(0)
        old_stdin, old_stdout, old_stderr = self._old_targets.pop()
        setattr(sys, "stdin", old_stdin)
        setattr(sys, "stdout", old_stdout)
        setattr(sys, "stderr", old_stderr)


def build_buffers(in_io_tty):
    """Build buffers for stdin stdout stderr that allows to catch binary/string data"""
    in_io = io.TextIOWrapper(io.BytesIO())
    # when stdin has pipeline data os.stdin.isatty() returns False
    in_io.isatty = lambda: in_io_tty
    out_io = io.TextIOWrapper(io.BytesIO())
    err_io = io.TextIOWrapper(io.BytesIO())
    return in_io, out_io, err_io

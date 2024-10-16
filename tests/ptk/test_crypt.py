import io
import secrets
from pathlib import Path
import pytest
from ptk.files import (
    iter_bytes,
    ChaChaCipher,
    AESCipher,
    FileFlipper,
    FileCryptor,
    KeyMan,
)


def test_iter_bytes():
    fp = io.BytesIO(b"hello")
    arr = list(iter_bytes(fp, 4))
    assert arr == [b"hell", b"o"]


@pytest.mark.parametrize("kls", [ChaChaCipher, AESCipher])
def test_cipher(kls):
    msg = b"hello"
    key = b"a" * 32
    cc = kls(key)
    pt = io.BytesIO(msg)
    ct = io.BytesIO()
    cc.encrypt(pt, ct)
    assert ct.getvalue() != pt.getvalue()

    pt.seek(0)
    ct.seek(0)
    cc.decrypt(ct, pt)
    assert pt.getvalue() == msg


def read_file(filename):
    with open(filename, "rb") as f:
        return f.read()


def test_flipper(tmp_path: Path):
    msg = secrets.token_bytes(256)
    filename = tmp_path / "hello.txt"
    with open(filename, "wb") as f:
        f.write(msg)

    ff = FileFlipper(128)

    ff.flip(filename)
    buf = read_file(filename)
    assert msg[:128] != buf[:128]
    assert msg[128:] == buf[128:]

    ff.flip(filename)
    buf = read_file(filename)
    assert msg == buf


def write_file(filename, content: bytes):
    with open(filename, "wb") as f:
        f.write(content)


def test_FileCryptor(tmp_path: Path):
    key = secrets.token_bytes(32)
    plain_file = tmp_path / "plain.dat"
    cipher_file = tmp_path / "cipher.dat"
    msg = b"Hello, World!"
    write_file(plain_file, msg)

    fc = FileCryptor(key, ChaChaCipher)
    buf = io.BytesIO()
    fc.encrypt(plain_file, buf)
    ctxt = buf.getvalue()
    assert ctxt
    write_file(cipher_file, ctxt)
    fc.decrypt(cipher_file, plain_file)
    assert msg == read_file(plain_file)

    fc.encrypt(plain_file, cipher_file)
    fc.decrypt(cipher_file, plain_file)
    assert msg == read_file(plain_file)


def test_KeyMan(tmp_path: Path):
    filename = tmp_path / "pass"
    pm = KeyMan(filename)
    assert not pm.load()
    pm.reset_passwd(b"testing")

    key = pm.load()
    assert len(key) == 32

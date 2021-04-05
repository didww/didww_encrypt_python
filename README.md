# DIDWW Encrypt Python3 SDK

This is Python 3 module and utility to encrypt file for DIDWW API 3.

File encrypted with mode `sandbox` could be uploaded to `POST https://sandbox-api.didww.com/v3/encrypted_files`.

File encrypted with mode `production` could be uploaded to `POST https://api.didww.com/v3/encrypted_files`.

see [DIDWW Documentation](https://doc.didww.com) for details.

## Requirements

Python `>=3.6`

## Dependencies

[PyCryptodomex](https://pypi.org/project/pycryptodomex/)

## Install

```shell
pip install didww_encrypt
```

## Usage

### Inside python
```python
from didww_encrypt import Encrypt


infile = open("doc.pdf", "rb")
enc = Encrypt.new("sandbox")
enc_data = enc.encrypt(infile.read())
outfile = open("doc.pdf.enc", "wb")
outfile.write(enc_data)
fingerprint = enc.fingerprint
```

### Shell

```
usage: didww_encrypt [-h] [-i [INPUT]] [-o [OUTPUT]] [-f] (-m [{sandbox,production}] | -u [URI])

Encrypt file for DIDWW API 3

optional arguments:
  -h, --help            show this help message and exit
  -i [INPUT], --input [INPUT]
                        use input pipe when not passed
  -o [OUTPUT], --output [OUTPUT]
                        use output pipe when not passed
  -f, --fingerprint     return fingerprint for public keys
  -m [{sandbox,production}], --mode [{sandbox,production}]
                        which DIDWW server use for public keys fetching
  -u [URI], --uri [URI]
                        custom URI for public keys fetching
```

You can pass input and output files as params
```shell
$ didww_encrypt -i ./doc.pdf -o ./doc.pdf.enc -m sandbox
```

Or using pipe
```shell
$ cat ./doc.pdf | didww_encrypt -m production > ./doc.pdf.enc
```

Also script could be run via `python -m`
```shell
$ python -m didww_encrypt -i ./doc.pdf -o ./doc.pdf.enc -m production
$ cat ./doc.pdf | python -m didww_encrypt -m sandbox > ./doc.pdf.enc
```

To print fingerprint use `-f` option instead of `-i`
```shell
$ didww_encrypt -f -mode sandbox
c74684d7863639169c21c4d04747f8d6fa05cfe3:::7c56fd5d2e1f2ada18765d936e74712037aea7eb
```

Or you can save it to a file
```shell
$ didww_encrypt -f -mode sandbox -o fingerprint.txt
```

**Keep in mind** that shell script returns fingerprint with newline which should be omitted when send it to `/v3/encrypted_files`.

## Additional information

both shell script and module function `Encrypt.new` respects `http_proxy` env variable when fetching public keys.

```shell
http_proxy="http://myproxy.example.com:1234" didww_encrypt -m sandbox
```
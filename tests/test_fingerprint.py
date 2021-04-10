import unittest
from didww_encrypt import fingerprint


pubkey_a = """-----BEGIN RSA PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA2t8H+QJMz+/y5NygzIAF
cdJnq/4x7seJPvlKTKeKLWWfiMqRefPYqfWn0sVDwzaKW4Eic8c68z+EzyDXTTa0
YHG+RmoN9m4W9wBVoZZrESskGSyLyB6mgc4kcv5PIdb3JbmdJJxNGslKUn8DeIin
j6VIt97hHSUVicf0QeA3W+nNpwAsnxCVn5mRTGlIYmmbi9RClWul/50XTcOMWPJf
3hkFBDuCJQlqO+HFqCmeRqWuoznHlVENBp2wAF8epCLiau1S9BUG4V5zrQrm6LvM
Fh6K9vCQyWAWTCNjiT8rfCcPXudzuznR7l0FnVMcJMqI2YxHw3yjHix+MH2SjZcr
eaawq9h6gTjDJArTqJZDv8jbvQqg+KXClz+2C1RhDATzT358LvcM8jRONc+tcnZd
fU1loNgslEy8V0zB1LxGjWWmAZ3Jqtb08WS3CAoKd2psQPz1MyaKXUl8r7v+ZTif
yG1+xDEgfyPTH1PuNQGBmPhu1KlhsUAG1i/m51FIMTkmV/n+BN9706InjWFsDvkS
Jbrp0PH94y+6LxTnRs1A3HcQbjuI5YbBeP2U867NpcWuDhNAC+z3XzBoTK0qlTPi
CvqR0iSB1IWgTS59VJIbDXOMTIBvn5/QUsQG4w8X0R+mP9XRH87spI9nX87Bv9za
tGvxOAVxjx+/BOLBZcS9nckCAwEAAQ==
-----END RSA PUBLIC KEY-----
"""
pubkey_b = """-----BEGIN RSA PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAvxO1LnsVQXtsiqHhDGpx
rsqL97AuPDU36B1Jj56R6600i920UfDk5QYXKN+xvjOycIcyzfl9CMAwusRcXFAn
nexv6WcB0ub8TT4bJ2C+citZp77ww35lTJRBUKBfljkP9x9gfZxnRRC8ySCoPnpW
qeoiVYQEG3St8s+VYL8vnSZwCE1TKctPFvdnpp9in7G5/iXhY666swulnBoaGEQN
f0+foQQKF7vVr8ZyDimIxpOHJf29O2h+qEMo98wje6T0/Nxk98JucIb8SquXTDwR
/LcbVVTfJO8uvxcPXwNMezPfKIHt0pMjQ2yLC7iQeHk6ZNe86ACBsBertiGiwoEc
wrJoYFUCD0M7Wlt6bm1AIREXbLHDnAYmj6e93d5pLlQe40savJg+nQX1/ESLlPiq
yE4M9rxgZdW5mt1PE9GJVXj5rZTU3AURp8PN0lrWtc8l3i2icn6zHPJMnYcBfNyh
vy7zcOsmmQnqBewrcviJZH26blPsDR17XK9bmjfAfriR+DxCllBdLgB6tCDKahwk
GquF5xFzAqukRi6Y14AqLvCBbs00sVQQDwbaTB3c4iAf4EHL+iSwedYWue0bA9R8
HmsNDhmmmNreToj4Zh9ERexSg1lCFUPGqrCnKKqO3BuoMQGkMl1ZY0gsxZ4qGJZA
F7Nkc8AJDVTsR/uZdATz1ckCAwEAAQ==
-----END RSA PUBLIC KEY-----"""


class TestFingerprint(unittest.TestCase):
    def test_fingerprint(self):
        result = fingerprint.calculate_fingerprint(pubkey_a, pubkey_b)
        self.assertEqual(
            "3cec19a8adf27cf0323d91640b98e9dc501f212b:::434f83703c899ed16329252940773da8fa38678c",
            result,
        )

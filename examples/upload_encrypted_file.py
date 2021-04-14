import os
import sys
import requests
from didww_encrypt import Encrypt, MODE_SANDBOX

file_path = os.environ.get("FILE_PATH")
if file_path is None:
    sys.stderr.write("Please provide FILE_PATH\n")
    exit(1)

with open(file_path, mode="rb") as f:
    data = f.read()

enc = Encrypt.new(MODE_SANDBOX)
enc_data = enc.encrypt(data)

api_key = os.environ.get("DIDWW_API_KEY")
if api_key is None:
    sys.stderr.write("Please provide DIDWW_API_KEY\n")
    exit(1)

response = requests.post(
    "https://sandbox-api.didww.com/v3/encrypted_files",
    headers={"Api-Key": api_key},
    files={"encrypted_files[items][][file]": enc_data},
    data={
        "encrypted_files[encryption_fingerprint]": enc.fingerprint,
        "encrypted_files[items][][description]": "python lib",
    },
)
print(f"Response: {response.status_code} #{response.json()}")

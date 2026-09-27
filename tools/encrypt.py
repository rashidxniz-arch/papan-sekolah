"""Usage: python3 tools/encrypt.py <plain.json> <PIN>
Writes data/board.enc.json: AES-256-GCM, key = PBKDF2-SHA256(PIN, salt, iter).
Never commit the plain JSON or the PIN."""
import sys, os, json, base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
src, pin = sys.argv[1], sys.argv[2]
ITER = 250000
salt, iv = os.urandom(16), os.urandom(12)
key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(pin.encode())
ct = AESGCM(key).encrypt(iv, open(src, 'rb').read(), None)
b = lambda x: base64.b64encode(x).decode()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'board.enc.json')
json.dump({'v': 1, 'iter': ITER, 'salt': b(salt), 'iv': b(iv), 'ct': b(ct)}, open(out, 'w'))
# verify
d = json.load(open(out)); k2 = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=base64.b64decode(d['salt']), iterations=d['iter']).derive(pin.encode())
assert AESGCM(k2).decrypt(base64.b64decode(d['iv']), base64.b64decode(d['ct']), None) == open(src, 'rb').read()
print('encrypted + verified ->', os.path.normpath(out))

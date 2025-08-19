import base64
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives import serialization
def generate_keypair():
priv = X25519PrivateKey.generate()
pub = priv.public_key()
alg = "X25519"
pub_bytes = pub.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
priv_bytes = priv.private_bytes(encoding=serialization.Encoding.Raw, format=serialization.PrivateFormat.Raw, encryption_algorithm=serialization.NoEncryption())
return alg, base64.b64encode(pub_bytes).decode(), base64.b64encode(priv_bytes).decode()

import hashlib
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()
def verify_password(p, h):
    return hash_password(p) == h
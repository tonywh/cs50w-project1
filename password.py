import hashlib, binascii, os

# Returns salt + password-hash ready for storing. 
def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    hash_bin = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    hash = binascii.hexlify(hash_bin)
    return (salt + hash).decode('ascii')
 
# Returns True on correct match
def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_hash = stored_password[64:]
    hash_bin = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    hash = binascii.hexlify(hash_bin).decode('ascii')
    return hash == stored_hash
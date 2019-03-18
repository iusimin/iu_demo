from passlib.context import CryptContext
import base64
'''

    Using pbkdf2_sha256 due to discussion found here:
    http://packages.python.org/passlib/new_app_quickstart.html#recommended-hashes

    Numbers choosen yielded the following results:
        ~120ms for encryption
        ~60ms for verification

    Processing time increases linearly with # of rounds
'''

_password_context = CryptContext(
    schemes                     = ["pbkdf2_sha256"],
    pbkdf2_sha256__salt_size    = 256, # bytes
    pbkdf2_sha256__rounds       = 16000,
)

def encrypt_password(password_raw):
    return _password_context.encrypt(password_raw)

def verify_password(password_hash, password_attempt):
    return _password_context.verify(password_attempt, password_hash)


_api_context = CryptContext(
    schemes                   = ["pbkdf2_sha1"],
    pbkdf2_sha1__salt_size    = 16, # bytes
    pbkdf2_sha1__rounds       = 100,
)

def encrypt_api_key(username, hashed_password):
    return _api_context.encrypt(username + hashed_password)

def verify_api_key(api_key, username, hashed_password):
    api_key = base64.b64decode(api_key)
    return _api_context.verify(username + hashed_password, api_key)
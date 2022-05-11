import binascii
import logging

from passlib.context import CryptContext


logger = logging.getLogger(__name__)


class PasswordEncryption:
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=["pbkdf2_sha512"],
            default="pbkdf2_sha512",
            pbkdf2_sha512__default_rounds=100000,
            pbkdf2_sha512__salt_size=16
        )

    def encrypt(self, plaintext_password):
        encrpyted_pass = self.pwd_context.encrypt(plaintext_password)

        return encrpyted_pass

    def verify(self, plaintext_password, hashed_password):
        try:

            return self.pwd_context.verify(plaintext_password, hashed_password)
        except binascii.Error as be:
            logger.error(be)

            return False
        except Exception as e:
            logger.error(str(e))

            return False

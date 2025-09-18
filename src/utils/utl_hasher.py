"""utility function for hashing passwords.

dsini kita memakai argon cffi.
"""

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from loguru import logger


class IHasher:
    """Interface for hasher."""

    def hash(self, password: str) -> str:
        """Hash the password."""
        raise NotImplementedError

    def verify(self, hashed_password: str, password: str) -> bool:
        """Verify the password against the hashed password."""
        raise NotImplementedError


class Argon2Hasher(IHasher):
    def __init__(self):
        self.ph = PasswordHasher()

    def hash(self, password: str) -> str:
        hashed = self.ph.hash(password)
        logger.debug(f"Hashed password: {hashed}")
        return hashed

    def verify(self, hashed_password: str, password: str) -> bool:
        try:
            is_verified = self.ph.verify(hashed_password, password)
            logger.debug(f"Password verification result: {is_verified}")
            return is_verified
        except VerifyMismatchError:
            logger.warning("Password verification failed.")
            return False


# singleton hasher instance
hasher = Argon2Hasher()


def get_hasher() -> IHasher:
    """Get the singleton hasher instance."""
    return hasher

from passlib.context import CryptContext

CRYPT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the plaintext password matches the hashed password
    :param plain_password:
    :param hashed_password:
    :return: verified password
    """
    return CRYPT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Get the hashed password
    :param password:
    :return: hashed password
    """
    return CRYPT.hash(password)

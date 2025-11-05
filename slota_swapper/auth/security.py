from passlib.context import CryptContext


# Use bcrypt_sha256 to avoid bcrypt's 72-byte password limit by pre-hashing with SHA256
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)



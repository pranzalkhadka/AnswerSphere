from passlib.context import CryptContext


# Use bcrypt for hashing the password
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")


def hash(password: str):
    # Hash the password
    return pwd_context.hash(password)



def verify(plain_password, hashed_password):
    # Verify the password by hashing the plain password and comparing it with the hashed password
    return pwd_context.verify(plain_password, hashed_password)
from pydoc import plain
from passlib.context import CryptContext #for hashing th password

pwd_context = CryptContext(schemes="bcrypt", deprecated = "auto") #telling passlib the default hashing algo to use

#func to hash the password
def hash(password: str):
    return pwd_context.hash(password)

#func to verify unhashed password is equal to hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
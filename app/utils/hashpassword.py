from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "Dosen1234"  # Change this to your desired password
hashed_password = pwd_context.hash(password)

print("Hashed Password:", hashed_password)

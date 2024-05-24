from dotenv import load_dotenv
import os

load_dotenv()

jwt_expiry = int(os.getenv("JWT_EXPIRY_HOUR", "168"))
host = os.getenv("PROTOCOL", "localhost")
db_url = os.getenv("DB_URL", "sqlite+aiosqlite:///../sqlite.db")
aaa = os.getenv("FIREBASE_PROJECT_ID", "aaa")

print(jwt_expiry)
print(host)
print(db_url)
print(aaa)
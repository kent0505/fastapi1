DB_HOST=""
DB_PORT=""
DB_USER=""
DB_PASS=""
DB_NAME=""
POSTGRES_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

HOST      = "localhost:8000" # change this to your domain
URL       = f"http://{HOST}" # change http to https
ORIGINS   = [f"https://{HOST}", f"https://www.{HOST}"]
DOCS_URL  = "/docs" # swagger url
USERNAME  = "admin" # admin username
PASSWORD  = "111" # admin password
KEY       = "" # jwt secret key
ALGORITHM = "HS256" # jwt algorithm
EXPIRY    = 24 # jwt expiry in hours

ws_clients = set()
ws_messages = []
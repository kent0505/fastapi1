HOST      = "localhost:8000" # change this to your domain
URL       = f"http://{HOST}" # change http to https
USERNAME  = "admin" # username
PASSWORD  = "$2b$12$bGLEyJqzf/3fboKkJeAVLurolqpuCnlS9HEj35qBFx0BaKpHTtTpO" # 111
KEY       = "" # jwt secret key
ORIGINS   = [f"https://{HOST}", f"https://www.{HOST}"]
DOCS_URL  = "/docs" # swagger url
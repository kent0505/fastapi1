HOST      = "localhost:8000" # change this to your domain
URL       = f"http://{HOST}" # change http to https
KEY       = "" # jwt secret key
ORIGINS   = [f"https://{HOST}", f"https://www.{HOST}"]
DOCS_URL  = "/docs" # swagger url
import logging

HOST     = "localhost:8000"
KEY      = ""
ORIGINS  = [f"https://{HOST}", f"https://www.{HOST}"]
DOCS_URL = "/docs"
FILENAME = "logfile.log"
LEVEL    = logging.INFO
FORMAT   = "%(asctime)s - %(levelname)s - %(message)s"
DATEFMT  = "%d-%m-%Y %H:%M:%S"
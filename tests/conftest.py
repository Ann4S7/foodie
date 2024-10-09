import os

from dotenv import load_dotenv

if os.environ.get("ENV") == "TEST":
    load_dotenv(".env_test")
else:
    load_dotenv()

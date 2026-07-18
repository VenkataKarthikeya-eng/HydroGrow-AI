import os
from dotenv import load_dotenv

# Set base path to find the .env file in the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = os.getenv("SECRET_KEY", "94c25785a9bc8d5fe6b92f7d3a04ef12411e74fbe6b14299b9cfcd1548e65e8a")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:antigravity@127.0.0.1:5432/hydrogrow")

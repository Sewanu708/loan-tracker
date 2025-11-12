import os
from dotenv import load_dotenv
load_dotenv()
class Config():
    FLASK_ENV=os.getenv('FLASK_ENV')
    DATABASE_URL=os.getenv('DATABASE_URL')
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
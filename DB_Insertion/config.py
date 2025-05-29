import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_config():
    return {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME")
    }

def connect_to_db():
    return mysql.connector.connect(**get_db_config())

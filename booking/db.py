import mysql.connector
from config import db_config

def connect_to_db():
    return mysql.connector.connect(**db_config)

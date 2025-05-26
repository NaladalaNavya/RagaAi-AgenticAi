import pymysql


def get_db_connection():
    """Create and return a new database connection."""
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Navya@2307',
        db='hospital_system',
        cursorclass=pymysql.cursors.DictCursor
    )

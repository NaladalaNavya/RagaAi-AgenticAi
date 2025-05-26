import pymysql

def get_mysql_connection():
    return pymysql.connect(
        host='localhost', 
        user='root', 
        password='Navya@2307', 
        db='hospital_system'
    )

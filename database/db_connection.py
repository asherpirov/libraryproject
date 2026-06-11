import mysql.connector

HOST = "localhost"
USER = "root"
PASSWORD = "secret"
DB = "db_library"
PORT = 3306

def get_connection()-> mysql.connector.connect:
    conn = mysql.connector.connect(host=HOST,
                                   user=USER,
                                   password=PASSWORD,
                                   database=DB,
                                   port=PORT)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    members_query = """
            CREATE TABLE IF NOT EXISTS members (  
            id INT AUTO_INCREMENT PRIMARY KEY,  
            email VARCHAR(50) UNIQUE,  
            name VARCHAR(50) NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            total_borrows INT NOT NULL DEFAULT 0
            )
                 """
    cursor.execute(members_query)
    conn.close()
    cursor.close()

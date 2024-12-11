import mysql.connector 
from config_app.config import DB_CONFIG

class Costumer:
    def __init__(self):
        self.connection = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()

    def count_users(self):
        query = "SELECT COUNT(*) FROM customer"  # Ajuste o nome da tabela conforme necessário
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

import mysql.connector

class SQLClient:
    def __init__(self, host="localhost", user="root", password="root", database="gestion_practicas"):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.conn.autocommit = True  # útil para pruebas
        self.cursor = self.conn.cursor(dictionary=True)  # devuelve dicts

    def fetchall(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def fetchone(self, query, params=None):
        self.cursor.execute(query, params or ())
        row = self.cursor.fetchone()
        return row

    def execute(self, query, params=None):
        """Para INSERT/UPDATE/DELETE"""
        self.cursor.execute(query, params or ())
        return self.cursor.rowcount

    def close(self):
        self.cursor.close()
        self.conn.close()

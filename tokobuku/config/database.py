import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self):
        self.host = "localhost"
        self.db_name = "tokobuku"
        self.username = "root"
        self.password = ""
        self.con = None

    def get_connection(self):
        try:
            # autocommit=True agar data terbaru dari model lain selalu terbaca
            self.con = mysql.connector.connect(
                host=self.host,
                database=self.db_name,
                user=self.username,
                password=self.password,
                autocommit=True
            )

            if self.con.is_connected():
                return self.con

        except Error as e:
            print(f"Koneksi gagal: {e}")
            return None

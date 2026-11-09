from mysql.connector import Error
from config.database import Database


class SupplierModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "supplier"

    def get_all_supplier(self):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name} ORDER BY id_supplier"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def create_supplier(self, nama, alamat, telepon):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"INSERT INTO {self.table_name} (nama_supplier, alamat, telepon) VALUES (%s, %s, %s)"
            cursor.execute(query, (nama, alamat, telepon))
            self.conn.commit()
            cursor.close()
            return True
        return False

    def update_supplier(self, id_supplier, nama, alamat, telepon):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"UPDATE {self.table_name} SET nama_supplier = %s, alamat = %s, telepon = %s WHERE id_supplier = %s"
            cursor.execute(query, (nama, alamat, telepon, id_supplier))
            self.conn.commit()
            cursor.close()
            return True
        return False

    def delete_supplier(self, id_supplier):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                query = f"DELETE FROM {self.table_name} WHERE id_supplier = %s"
                cursor.execute(query, (id_supplier,))
                self.conn.commit()
                cursor.close()
                return True
            except Error as e:
                # Gagal jika supplier masih dipakai oleh data buku (foreign key)
                print(f"Hapus gagal: {e}")
                return False
        return False

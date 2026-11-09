from mysql.connector import Error
from config.database import Database


class BukuModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "buku"

    def get_all_buku(self):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = (f"SELECT b.*, s.nama_supplier FROM {self.table_name} b "
                     "LEFT JOIN supplier s ON b.id_supplier = s.id_supplier ORDER BY b.id_buku")
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def create_buku(self, judul, penulis, kategori, harga, stok, id_supplier):
        if self.conn:
            cursor = self.conn.cursor()
            query = (f"INSERT INTO {self.table_name} (judul, penulis, kategori, harga, stok, id_supplier) "
                     "VALUES (%s, %s, %s, %s, %s, %s)")
            val = (judul, penulis, kategori, harga, stok, id_supplier)
            cursor.execute(query, val)
            self.conn.commit()
            cursor.close()
            return True
        return False

    def update_buku(self, id_buku, judul, penulis, kategori, harga, stok, id_supplier):
        if self.conn:
            cursor = self.conn.cursor()
            query = (f"UPDATE {self.table_name} SET judul = %s, penulis = %s, kategori = %s, "
                     "harga = %s, stok = %s, id_supplier = %s WHERE id_buku = %s")
            val = (judul, penulis, kategori, harga, stok, id_supplier, id_buku)
            cursor.execute(query, val)
            self.conn.commit()
            cursor.close()
            return True
        return False

    def delete_buku(self, id_buku):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                query = f"DELETE FROM {self.table_name} WHERE id_buku = %s"
                cursor.execute(query, (id_buku,))
                self.conn.commit()
                cursor.close()
                return True
            except Error as e:
                # Gagal jika buku sudah tercatat pada transaksi (foreign key)
                print(f"Hapus gagal: {e}")
                return False
        return False

    def tambah_stok(self, id_buku, jumlah):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"UPDATE {self.table_name} SET stok = stok + %s WHERE id_buku = %s"
            cursor.execute(query, (jumlah, id_buku))
            self.conn.commit()
            cursor.close()
            return True
        return False

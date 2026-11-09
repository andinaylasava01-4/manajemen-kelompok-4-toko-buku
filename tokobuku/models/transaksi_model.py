from mysql.connector import Error
from config.database import Database


class TransaksiModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "transaksi"

    def simpan_transaksi(self, id_akun, keranjang, total, bayar):
        """Simpan transaksi + detailnya + kurangi stok dalam satu transaksi database."""
        if self.conn:
            cursor = self.conn.cursor()
            try:
                self.conn.start_transaction()
                kembalian = bayar - total
                query = (f"INSERT INTO {self.table_name} (tanggal, id_akun, total, bayar, kembalian) "
                         "VALUES (NOW(), %s, %s, %s, %s)")
                cursor.execute(query, (id_akun, total, bayar, kembalian))
                id_transaksi = cursor.lastrowid

                for item in keranjang:
                    subtotal = item["harga"] * item["jumlah"]
                    cursor.execute(
                        "INSERT INTO detail_transaksi (id_transaksi, id_buku, jumlah, harga, subtotal) "
                        "VALUES (%s, %s, %s, %s, %s)",
                        (id_transaksi, item["id_buku"], item["jumlah"], item["harga"], subtotal))
                    cursor.execute(
                        "UPDATE buku SET stok = stok - %s WHERE id_buku = %s AND stok >= %s",
                        (item["jumlah"], item["id_buku"], item["jumlah"]))
                    if cursor.rowcount == 0:
                        raise Error("Stok tidak cukup")

                self.conn.commit()
                return id_transaksi
            except Error as e:
                # Batalkan semua perubahan jika ada yang gagal
                self.conn.rollback()
                print(f"Transaksi gagal: {e}")
                return None
            finally:
                cursor.close()
        return None

    def get_all_transaksi(self):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = (f"SELECT t.id_transaksi, t.tanggal, a.nama AS kasir, t.total, t.bayar, t.kembalian "
                     f"FROM {self.table_name} t JOIN akun a ON t.id_akun = a.id_akun "
                     "ORDER BY t.tanggal DESC, t.id_transaksi DESC")
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def get_transaksi(self, id_transaksi):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = (f"SELECT t.id_transaksi, t.tanggal, a.nama AS kasir, t.total, t.bayar, t.kembalian "
                     f"FROM {self.table_name} t JOIN akun a ON t.id_akun = a.id_akun "
                     "WHERE t.id_transaksi = %s")
            cursor.execute(query, (id_transaksi,))
            result = cursor.fetchone()
            cursor.close()
            return result
        return None

    def get_detail(self, id_transaksi):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = ("SELECT d.jumlah, d.harga, d.subtotal, b.judul FROM detail_transaksi d "
                     "JOIN buku b ON d.id_buku = b.id_buku WHERE d.id_transaksi = %s")
            cursor.execute(query, (id_transaksi,))
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

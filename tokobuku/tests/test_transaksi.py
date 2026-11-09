from unittest.mock import MagicMock
from models.transaksi_model import TransaksiModel

KERANJANG = [
    {"id_buku": 1, "judul": "Laskar Pelangi", "harga": 89000, "jumlah": 2},
    {"id_buku": 2, "judul": "Bumi Manusia", "harga": 120000, "jumlah": 1},
]


def test_simpan_transaksi_berhasil():
    model = TransaksiModel()
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.lastrowid = 7
    mock_cursor.rowcount = 1  # update stok berhasil
    model.conn.cursor.return_value = mock_cursor

    hasil = model.simpan_transaksi(2, KERANJANG, 298000, 300000)

    # Mengembalikan id transaksi yang baru dibuat
    assert hasil == 7

    # 1 insert transaksi + (insert detail + update stok) untuk 2 item = 5 query
    assert mock_cursor.execute.call_count == 5
    model.conn.commit.assert_called_once()


def test_simpan_transaksi_stok_kurang_rollback():
    model = TransaksiModel()
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.lastrowid = 8
    mock_cursor.rowcount = 0  # update stok gagal (stok tidak cukup)
    model.conn.cursor.return_value = mock_cursor

    hasil = model.simpan_transaksi(2, KERANJANG, 298000, 300000)

    assert hasil is None
    model.conn.rollback.assert_called_once()
    model.conn.commit.assert_not_called()

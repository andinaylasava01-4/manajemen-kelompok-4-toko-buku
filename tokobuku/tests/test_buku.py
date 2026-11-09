from unittest.mock import MagicMock
from models.buku_model import BukuModel


def test_create_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()

    # Memanipulasi (Mock) koneksi database agar tidak mengotori data asli
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Melakukan eksekusi fungsi
    hasil = model.create_buku("Buku Testing", "Penulis QA", "Novel", 50000, 10, 1)

    # Memverifikasi apakah fungsi mengembalikan nilai True
    assert hasil is True

    # Memverifikasi apakah cursor.execute benar-benar dipanggil
    mock_cursor.execute.assert_called_once()

    # Memverifikasi apakah perintah commit (simpan) dipanggil
    model.conn.commit.assert_called_once()


def test_tambah_stok_berhasil():
    model = BukuModel()
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    hasil = model.tambah_stok(1, 5)

    assert hasil is True
    mock_cursor.execute.assert_called_once()
    model.conn.commit.assert_called_once()

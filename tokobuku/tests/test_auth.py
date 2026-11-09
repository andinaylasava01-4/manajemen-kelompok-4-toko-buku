from unittest.mock import MagicMock
from models.akun_model import AkunModel


def test_hash_password_konsisten():
    password_asli = "admin123"
    hash_1 = AkunModel.hash_password(password_asli)
    hash_2 = AkunModel.hash_password(password_asli)

    # Memastikan hasil hash tidak sama dengan plain text dan bersifat konsisten
    assert hash_1 != password_asli
    assert hash_1 == hash_2
    assert len(hash_1) == 64  # Panjang karakter standar SHA-256


def test_autentikasi_pengguna_berhasil():
    model = AkunModel()
    model.conn = MagicMock()
    mock_cursor = MagicMock()

    # Simulasi kembalian data dari database ketika username & password cocok
    mock_cursor.fetchone.return_value = {
        "id_akun": 1,
        "username": "admin",
        "nama": "Administrator",
        "role": "admin"
    }
    model.conn.cursor.return_value = mock_cursor

    hasil = model.autentikasi("admin", "admin123")

    assert hasil is not None
    assert hasil["username"] == "admin"
    assert hasil["role"] == "admin"


def test_autentikasi_pengguna_gagal():
    model = AkunModel()
    model.conn = MagicMock()
    mock_cursor = MagicMock()

    # Simulasi database tidak menemukan data (username/password salah)
    mock_cursor.fetchone.return_value = None
    model.conn.cursor.return_value = mock_cursor

    hasil = model.autentikasi("admin", "salah")

    assert hasil is None

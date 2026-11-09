from models.buku_model import BukuModel
from views.daftar_buku_view import DaftarBukuView

BATAS_STOK = 5  # stok sama dengan atau di bawah angka ini dianggap menipis


class DaftarBukuController:
    def __init__(self, parent, judul):
        self.model = BukuModel()
        self.view = DaftarBukuView(parent, judul)
        self.view.pack(fill="both", expand=True)
        self.refresh()

    def refresh(self):
        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        for buku in self.model.get_all_buku():
            menipis = buku['stok'] <= BATAS_STOK
            status = "Menipis" if menipis else "Aman"
            self.view.tabel.insert("", "end", values=(
                buku['id_buku'], buku['judul'], buku['penulis'], buku['kategori'],
                buku['harga'], buku['stok'], status),
                tags=("menipis",) if menipis else ())

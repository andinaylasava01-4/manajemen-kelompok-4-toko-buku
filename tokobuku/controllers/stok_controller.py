import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.stok_view import StokView
from views.pencarian import PencarianBuku


class StokController:
    def __init__(self, parent):
        self.model = BukuModel()
        self.view = StokView(parent)
        self.view.pack(fill="both", expand=True)
        self.data_buku = []
        self.pencarian = PencarianBuku(self.view.combo_buku)

        self.view.btn_tambah.configure(command=self.tambah_stok)
        self.refresh()

    def refresh(self):
        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        self.data_buku = self.model.get_all_buku()

        for buku in self.data_buku:
            self.view.tabel.insert("", "end", values=(
                buku['id_buku'], buku['judul'], buku['nama_supplier'], buku['stok']))

        # Isi pilihan buku pada combo box
        pilihan = [f"{b['id_buku']} - {b['judul']}" for b in self.data_buku]
        self.pencarian.set_pilihan(pilihan)

    def tambah_stok(self):
        pilihan = self.view.combo_buku.get()
        jumlah = self.view.entry_jumlah.get()

        if not pilihan or not jumlah:
            messagebox.showwarning("Peringatan", "Pilih buku dan isi jumlah stok!")
            return

        if not jumlah.isdigit() or int(jumlah) <= 0:
            messagebox.showwarning("Peringatan", "Jumlah stok harus berupa angka lebih dari 0!")
            return

        id_buku = self.pencarian.ambil_id()
        if id_buku is None:
            messagebox.showwarning("Peringatan", "Buku tidak ditemukan atau belum jelas. Ketik judul lebih lengkap atau pilih dari daftar!")
            return

        if self.model.tambah_stok(id_buku, int(jumlah)):
            messagebox.showinfo("Sukses", "Stok buku berhasil ditambah!")
            self.view.entry_jumlah.delete(0, 'end')
            self.pencarian.reset()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menambah stok.")

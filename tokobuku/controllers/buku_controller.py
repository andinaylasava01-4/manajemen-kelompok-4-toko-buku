import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from models.supplier_model import SupplierModel
from views.buku_view import BukuView
from views.pencarian import PencarianBuku, ComboBoxFilter


class BukuController:
    def __init__(self, parent):
        self.model = BukuModel()
        self.supplier_model = SupplierModel()
        self.view = BukuView(parent)
        self.view.pack(fill="both", expand=True)

        self.id_terpilih = None
        self.data_buku = []
        self.pencarian_supplier = PencarianBuku(self.view.combo_supplier)
        self.filter_kategori = ComboBoxFilter(self.view.combo_kategori)

        # Binding (mengikat) tombol di View dengan fungsi di Controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_ubah.configure(command=self.ubah_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        self.view.btn_bersihkan.configure(command=self.bersihkan_form)
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_baris)

        self.refresh()

    def refresh(self):
        self.muat_supplier()
        self.muat_data_tabel()
        self.muat_kategori()

    def muat_supplier(self):
        daftar = self.supplier_model.get_all_supplier()
        pilihan = [f"{s['id_supplier']} - {s['nama_supplier']}" for s in daftar]
        self.pencarian_supplier.set_pilihan(pilihan)

    def muat_kategori(self):
        default = ["Novel", "Pelajaran", "Komputer", "Anak-anak"]
        dipakai = {b["kategori"] for b in self.data_buku}
        self.filter_kategori.set_pilihan(sorted(set(default) | dipakai))

    def muat_data_tabel(self):
        # Mengosongkan isi tabel di View terlebih dahulu
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        # Mengambil data dari Model (database)
        self.data_buku = self.model.get_all_buku()

        # Memasukkan data baru ke dalam tabel View
        for buku in self.data_buku:
            self.view.tabel.insert("", "end", values=(
                buku['id_buku'], buku['judul'], buku['penulis'], buku['kategori'],
                buku['harga'], buku['stok'], buku['nama_supplier']))

    def pilih_baris(self, event=None):
        pilihan = self.view.tabel.selection()
        if not pilihan:
            return
        id_buku = int(self.view.tabel.item(pilihan[0])["values"][0])

        for buku in self.data_buku:
            if buku["id_buku"] == id_buku:
                self.id_terpilih = id_buku
                self.isi_form(buku)
                break

    def isi_form(self, buku):
        self.kosongkan_form()
        self.view.entry_judul.insert(0, buku["judul"])
        self.view.entry_penulis.insert(0, buku["penulis"])
        self.view.combo_kategori.set(buku["kategori"])
        self.view.entry_harga.insert(0, str(buku["harga"]))
        self.view.entry_stok.insert(0, str(buku["stok"]))
        self.view.combo_supplier.set(f"{buku['id_supplier']} - {buku['nama_supplier']}")

    def kosongkan_form(self):
        self.view.entry_judul.delete(0, 'end')
        self.view.entry_penulis.delete(0, 'end')
        self.filter_kategori.reset()
        self.view.entry_harga.delete(0, 'end')
        self.view.entry_stok.delete(0, 'end')
        self.pencarian_supplier.reset()

    def bersihkan_form(self):
        self.id_terpilih = None
        self.kosongkan_form()
        self.view.tabel.selection_remove(self.view.tabel.selection())

    def ambil_form(self):
        # Mengambil teks dari kotak input di View
        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        kategori = self.view.combo_kategori.get()
        harga = self.view.entry_harga.get()
        stok = self.view.entry_stok.get()
        supplier = self.view.combo_supplier.get()

        # Validasi Form Kosong
        if not judul or not penulis or not kategori or not harga or not stok or not supplier:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return None

         # Validasi harga dan stok harus berupa angka
        if not harga.isdigit() or not stok.isdigit():
            messagebox.showwarning("Peringatan", "Harga dan Stok harus berupa angka!")
            return None
        
        id_supplier = self.pencarian_supplier.ambil_id()
        if id_supplier is None:
            messagebox.showwarning("Peringatan", "Supplier tidak ditemukan. Ketik nama lebih lengkap atau pilih dari daftar!")
            return None

        return judul, penulis, kategori, int(harga), int(stok), id_supplier

    def simpan_data(self):
        data = self.ambil_form()
        if data is None:
            return

        # Mengirim data ke Model untuk disimpan
        berhasil = self.model.create_buku(*data)
        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")

    def ubah_data(self):
        if self.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih buku pada tabel terlebih dahulu!")
            return

        data = self.ambil_form()
        if data is None:
            return

        berhasil = self.model.update_buku(self.id_terpilih, *data)
        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil diubah!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat mengubah data.")

    def hapus_data(self):
        if self.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih buku pada tabel terlebih dahulu!")
            return

        if not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus buku ini?"):
            return

        berhasil = self.model.delete_buku(self.id_terpilih)
        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Buku tidak dapat dihapus karena sudah tercatat pada transaksi.")

import tkinter.messagebox as messagebox
from models.supplier_model import SupplierModel
from views.supplier_view import SupplierView


class SupplierController:
    def __init__(self, parent):
        self.model = SupplierModel()
        self.view = SupplierView(parent)
        self.view.pack(fill="both", expand=True)

        self.id_terpilih = None
        self.data_supplier = []

        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_ubah.configure(command=self.ubah_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        self.view.btn_bersihkan.configure(command=self.bersihkan_form)
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_baris)

        self.refresh()

    def refresh(self):
        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        self.data_supplier = self.model.get_all_supplier()

        for s in self.data_supplier:
            self.view.tabel.insert("", "end", values=(
                s['id_supplier'], s['nama_supplier'], s['alamat'], s['telepon']))

    def pilih_baris(self, event=None):
        pilihan = self.view.tabel.selection()
        if not pilihan:
            return
        id_supplier = int(self.view.tabel.item(pilihan[0])["values"][0])

        for s in self.data_supplier:
            if s["id_supplier"] == id_supplier:
                self.id_terpilih = id_supplier
                self.kosongkan_form()
                self.view.entry_nama.insert(0, s["nama_supplier"])
                self.view.entry_alamat.insert(0, s["alamat"])
                self.view.entry_telepon.insert(0, s["telepon"])
                break

    def kosongkan_form(self):
        self.view.entry_nama.delete(0, 'end')
        self.view.entry_alamat.delete(0, 'end')
        self.view.entry_telepon.delete(0, 'end')

    def bersihkan_form(self):
        self.id_terpilih = None
        self.kosongkan_form()
        self.view.tabel.selection_remove(self.view.tabel.selection())

    def ambil_form(self):
        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()
        telepon = self.view.entry_telepon.get()

        # Validasi Form Kosong
        if not nama or not alamat or not telepon:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return None
        return nama, alamat, telepon

    def simpan_data(self):
        data = self.ambil_form()
        if data is None:
            return

        if self.model.create_supplier(*data):
            messagebox.showinfo("Sukses", "Data supplier berhasil disimpan!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")

    def ubah_data(self):
        if self.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih supplier pada tabel terlebih dahulu!")
            return

        data = self.ambil_form()
        if data is None:
            return

        if self.model.update_supplier(self.id_terpilih, *data):
            messagebox.showinfo("Sukses", "Data supplier berhasil diubah!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat mengubah data.")

    def hapus_data(self):
        if self.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih supplier pada tabel terlebih dahulu!")
            return

        if not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus supplier ini?"):
            return

        if self.model.delete_supplier(self.id_terpilih):
            messagebox.showinfo("Sukses", "Data supplier berhasil dihapus!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Supplier tidak dapat dihapus karena masih dipakai data buku.")

import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from models.transaksi_model import TransaksiModel
from views.transaksi_view import TransaksiView
from views.pencarian import PencarianBuku
from controllers.struk_controller import StrukController, rupiah


class TransaksiController:
    def __init__(self, parent, user):
        self.user = user
        self.buku_model = BukuModel()
        self.model = TransaksiModel()
        self.view = TransaksiView(parent)
        self.view.pack(fill="both", expand=True)

        self.data_buku = []
        self.keranjang = []  # setiap item: id_buku, judul, harga, jumlah
        self.pencarian = PencarianBuku(self.view.combo_buku)

        self.view.btn_tambah.configure(command=self.tambah_item)
        self.view.btn_hapus_item.configure(command=self.hapus_item)
        self.view.btn_bayar.configure(command=self.bayar)
        self.view.seg_metode.configure(command=self.ganti_metode)

        self.refresh()

    def refresh(self):
        # Muat ulang daftar buku (stok terbaru) pada combo box
        self.data_buku = self.buku_model.get_all_buku()
        pilihan = [f"{b['id_buku']} - {b['judul']} (stok {b['stok']})" for b in self.data_buku]
        self.pencarian.set_pilihan(pilihan)
        self.pencarian.reset()

    def cari_buku(self, id_buku):
        for buku in self.data_buku:
            if buku["id_buku"] == id_buku:
                return buku
        return None

    def total(self):
        return sum(item["harga"] * item["jumlah"] for item in self.keranjang)

    def muat_keranjang(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        for item in self.keranjang:
            self.view.tabel.insert("", "end", values=(
                item["id_buku"], item["judul"], item["harga"], item["jumlah"],
                item["harga"] * item["jumlah"]))

        self.view.label_total.configure(text=f"Total: {rupiah(self.total())}")

    def tambah_item(self):
        pilihan = self.view.combo_buku.get()
        jumlah = self.view.entry_jumlah.get()

        if not pilihan or not jumlah:
            messagebox.showwarning("Peringatan", "Pilih buku dan isi jumlah beli!")
            return

        if not jumlah.isdigit() or int(jumlah) <= 0:
            messagebox.showwarning("Peringatan", "Jumlah beli harus berupa angka lebih dari 0!")
            return

        id_buku = self.pencarian.ambil_id()
        if id_buku is None:
            messagebox.showwarning("Peringatan", "Buku tidak ditemukan atau belum jelas. Ketik judul lebih lengkap atau pilih dari daftar!")
            return

        buku = self.cari_buku(id_buku)
        jumlah = int(jumlah)

        # Jumlah yang sudah ada di keranjang ikut dihitung saat cek stok
        sudah_ada = None
        for item in self.keranjang:
            if item["id_buku"] == id_buku:
                sudah_ada = item

        jumlah_total = jumlah + (sudah_ada["jumlah"] if sudah_ada else 0)
        if jumlah_total > buku["stok"]:
            messagebox.showerror("Stok Tidak Cukup", f"Stok '{buku['judul']}' hanya {buku['stok']}.")
            return

        if sudah_ada:
            sudah_ada["jumlah"] = jumlah_total
        else:
            self.keranjang.append({
                "id_buku": id_buku,
                "judul": buku["judul"],
                "harga": buku["harga"],
                "jumlah": jumlah
            })

        self.view.entry_jumlah.delete(0, 'end')
        self.pencarian.reset()
        self.muat_keranjang()

    def hapus_item(self):
        pilihan = self.view.tabel.selection()
        if not pilihan:
            messagebox.showwarning("Peringatan", "Pilih item pada keranjang terlebih dahulu!")
            return

        id_buku = int(self.view.tabel.item(pilihan[0])["values"][0])
        self.keranjang = [item for item in self.keranjang if item["id_buku"] != id_buku]
        self.muat_keranjang()

    def ganti_metode(self, metode):
        # Tunai: kolom uang dibayar tampil. Non Tunai: kolom disembunyikan.
        if metode == "Tunai":
            self.view.entry_bayar.pack(side="right", padx=10, pady=10, before=self.view.seg_metode)
        else:
            self.view.entry_bayar.delete(0, 'end')
            self.view.entry_bayar.pack_forget()

    def bayar(self):
        if not self.keranjang:
            messagebox.showwarning("Peringatan", "Keranjang masih kosong!")
            return

        metode = self.view.seg_metode.get()
        total = self.total()

        if metode == "Tunai":
            bayar = self.view.entry_bayar.get()
            if not bayar.isdigit():
                messagebox.showwarning("Peringatan", "Uang dibayar harus berupa angka!")
                return

            bayar = int(bayar)
            if bayar < total:
                messagebox.showerror("Uang Kurang", f"Uang dibayar kurang dari total {rupiah(total)}.")
                return
        else:
            # Non tunai: pembayaran pas sesuai total, tanpa input nominal
            bayar = total

        id_transaksi = self.model.simpan_transaksi(self.user["id_akun"], self.keranjang, total, bayar)
        if id_transaksi:
            transaksi = self.model.get_transaksi(id_transaksi)
            detail = self.model.get_detail(id_transaksi)

            # Kosongkan keranjang dan muat ulang stok terbaru
            self.keranjang = []
            self.view.entry_bayar.delete(0, 'end')
            self.muat_keranjang()
            self.refresh()

            if metode == "Tunai":
                messagebox.showinfo("Sukses", f"Transaksi berhasil! Kembalian: {rupiah(transaksi['kembalian'])}")
            # Non tunai langsung menampilkan struk
            StrukController.tampilkan(self.view.winfo_toplevel(), transaksi, detail, metode)
        else:
            messagebox.showerror("Error", "Transaksi gagal disimpan. Periksa stok buku.")
            self.refresh()

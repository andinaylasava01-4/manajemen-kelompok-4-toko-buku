import tkinter.messagebox as messagebox
from views.main_view import MainView
from controllers.buku_controller import BukuController
from controllers.supplier_controller import SupplierController
from controllers.stok_controller import StokController
from controllers.daftar_buku_controller import DaftarBukuController
from controllers.transaksi_controller import TransaksiController
from controllers.laporan_controller import LaporanController


# OTORISASI: menu (tab) yang boleh diakses tiap role, sesuai use case diagram
HAK_AKSES = {
    "admin": ["Data Buku", "Supplier", "Stok Buku"],
    "kasir": ["Transaksi", "Buku & Stok", "Laporan"],
    "pemilik": ["Laporan", "Persediaan"],
}


class MainController:
    def __init__(self, user):
        self.user = user
        self.view = MainView(user["nama"], user["role"])
        self.controllers = {}
        self.logout_diminta = False
        self.view.btn_logout.configure(command=self.logout)

        # Hanya buat tab yang menjadi hak akses role pengguna
        for nama_tab in HAK_AKSES[user["role"]]:
            frame = self.view.tambah_tab(nama_tab)
            self.controllers[nama_tab] = self.buat_controller(nama_tab, frame)

        # Setiap pindah tab, data pada tab tersebut dimuat ulang
        self.view.tabview.configure(command=self.saat_tab_berganti)

    def buat_controller(self, nama_tab, frame):
        if nama_tab == "Data Buku":
            return BukuController(frame)
        if nama_tab == "Supplier":
            return SupplierController(frame)
        if nama_tab == "Stok Buku":
            return StokController(frame)
        if nama_tab == "Transaksi":
            return TransaksiController(frame, self.user)
        if nama_tab == "Buku & Stok":
            return DaftarBukuController(frame, "Daftar Buku dan Stok")
        if nama_tab == "Persediaan":
            return DaftarBukuController(frame, "Persediaan Buku")
        if nama_tab == "Laporan":
            return LaporanController(frame, self.user["role"])

    def saat_tab_berganti(self):
        self.controllers[self.view.tabview.get()].refresh()

    def logout(self):
        if messagebox.askyesno("Logout", "Yakin ingin logout?"):
            self.logout_diminta = True
            self.view.destroy()

    def run(self):
        self.view.mainloop()

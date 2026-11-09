import customtkinter as ctk
from tkinter import ttk


class DaftarBukuView(ctk.CTkFrame):
    """Tabel buku + stok (hanya lihat). Dipakai kasir (Buku & Stok) dan pemilik (Persediaan)."""

    def __init__(self, parent, judul="Daftar Buku dan Stok"):
        super().__init__(parent)

        ctk.CTkLabel(self, text=judul, font=("Arial", 16, "bold")).pack(pady=15)

        kolom = ("id", "judul", "penulis", "kategori", "harga", "stok", "status")
        self.tabel = ttk.Treeview(self, columns=kolom, show="headings", height=15)

        self.tabel.heading("id", text="ID")
        self.tabel.heading("judul", text="Judul Buku")
        self.tabel.heading("penulis", text="Penulis")
        self.tabel.heading("kategori", text="Kategori")
        self.tabel.heading("harga", text="Harga")
        self.tabel.heading("stok", text="Stok")
        self.tabel.heading("status", text="Status Stok")

        self.tabel.column("id", width=40, anchor="center")
        self.tabel.column("judul", width=250)
        self.tabel.column("penulis", width=150)
        self.tabel.column("kategori", width=100)
        self.tabel.column("harga", width=100, anchor="e")
        self.tabel.column("stok", width=60, anchor="center")
        self.tabel.column("status", width=100, anchor="center")

        # Baris dengan stok menipis ditandai warna merah
        self.tabel.tag_configure("menipis", foreground="red")

        self.tabel.pack(fill="both", expand=True, padx=15, pady=(0, 10))


if __name__ == "__main__":
    app = ctk.CTk()
    DaftarBukuView(app).pack(fill="both", expand=True)
    app.mainloop()

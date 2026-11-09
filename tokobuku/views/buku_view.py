import customtkinter as ctk
from tkinter import ttk


class BukuView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Konfigurasi Utama (1 Baris, 2 Kolom)
        self.grid_columnconfigure(0, weight=1)  # Kolom Kiri (Form)
        self.grid_columnconfigure(1, weight=3)  # Kolom Kanan (Tabel lebih lebar)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # FRAME KIRI: FORMULIR INPUT BUKU
        # ==========================================
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            self.frame_kiri,
            text="Form Data Buku",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.entry_judul = ctk.CTkEntry(self.frame_kiri, placeholder_text="Judul Buku")
        self.entry_judul.pack(pady=5, padx=15, fill="x")

        self.entry_penulis = ctk.CTkEntry(self.frame_kiri, placeholder_text="Nama Penulis")
        self.entry_penulis.pack(pady=5, padx=15, fill="x")

        # Kategori bisa dipilih dari daftar atau diketik untuk kategori baru
        ctk.CTkLabel(self.frame_kiri, text="Kategori").pack(padx=15, anchor="w")
        self.combo_kategori = ctk.CTkComboBox(
            self.frame_kiri,
            values=["Novel", "Pelajaran", "Komputer", "Anak-anak"]
        )
        self.combo_kategori.set("")
        self.combo_kategori.pack(pady=5, padx=15, fill="x")

        self.entry_harga = ctk.CTkEntry(self.frame_kiri, placeholder_text="Harga (Misal: 89000)")
        self.entry_harga.pack(pady=5, padx=15, fill="x")

        self.entry_stok = ctk.CTkEntry(self.frame_kiri, placeholder_text="Stok (Misal: 10)")
        self.entry_stok.pack(pady=5, padx=15, fill="x")

        ctk.CTkLabel(self.frame_kiri, text="Cari Supplier (ketik nama)").pack(padx=15, anchor="w")
        self.combo_supplier = ctk.CTkComboBox(self.frame_kiri, values=[""])
        self.combo_supplier.pack(pady=5, padx=15, fill="x")

        # Tombol Aksi
        self.btn_simpan = ctk.CTkButton(self.frame_kiri, text="Simpan Data", fg_color="green")
        self.btn_simpan.pack(pady=(15, 5), padx=15, fill="x")

        self.btn_ubah = ctk.CTkButton(self.frame_kiri, text="Ubah Data", fg_color="blue")
        self.btn_ubah.pack(pady=5, padx=15, fill="x")

        self.btn_hapus = ctk.CTkButton(self.frame_kiri, text="Hapus Data", fg_color="red")
        self.btn_hapus.pack(pady=5, padx=15, fill="x")

        self.btn_bersihkan = ctk.CTkButton(self.frame_kiri, text="Bersihkan Form", fg_color="gray")
        self.btn_bersihkan.pack(pady=5, padx=15, fill="x")

        # ==========================================
        # FRAME KANAN: TABEL DAFTAR BUKU
        # ==========================================
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            self.frame_kanan,
            text="Daftar Koleksi Buku",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        kolom = ("id", "judul", "penulis", "kategori", "harga", "stok", "supplier")
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=15)

        self.tabel.heading("id", text="ID")
        self.tabel.heading("judul", text="Judul Buku")
        self.tabel.heading("penulis", text="Penulis")
        self.tabel.heading("kategori", text="Kategori")
        self.tabel.heading("harga", text="Harga")
        self.tabel.heading("stok", text="Stok")
        self.tabel.heading("supplier", text="Supplier")

        self.tabel.column("id", width=35, anchor="center")
        self.tabel.column("judul", width=170)
        self.tabel.column("penulis", width=110)
        self.tabel.column("kategori", width=80)
        self.tabel.column("harga", width=70, anchor="e")
        self.tabel.column("stok", width=40, anchor="center")
        self.tabel.column("supplier", width=120)

        self.tabel.pack(fill="both", expand=True, padx=15, pady=(0, 10))


# Blok eksekusi untuk menjalankan view secara mandiri
if __name__ == "__main__":
    app = ctk.CTk()
    BukuView(app).pack(fill="both", expand=True)
    app.mainloop()

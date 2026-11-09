import customtkinter as ctk
from tkinter import ttk


class StokView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # FRAME KIRI: FORM TAMBAH STOK
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            self.frame_kiri,
            text="Tambah Stok Buku",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        ctk.CTkLabel(self.frame_kiri, text="Cari Buku (ketik judul / ID)").pack(padx=15, anchor="w")
        self.combo_buku = ctk.CTkComboBox(self.frame_kiri, values=[""])
        self.combo_buku.pack(pady=10, padx=15, fill="x")

        self.entry_jumlah = ctk.CTkEntry(self.frame_kiri, placeholder_text="Jumlah stok masuk")
        self.entry_jumlah.pack(pady=10, padx=15, fill="x")

        self.btn_tambah = ctk.CTkButton(self.frame_kiri, text="Tambah Stok", fg_color="green")
        self.btn_tambah.pack(pady=20, padx=15, fill="x")

        # FRAME KANAN: TABEL STOK
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            self.frame_kanan,
            text="Stok Buku Saat Ini",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        kolom = ("id", "judul", "supplier", "stok")
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=15)

        self.tabel.heading("id", text="ID")
        self.tabel.heading("judul", text="Judul Buku")
        self.tabel.heading("supplier", text="Supplier")
        self.tabel.heading("stok", text="Stok")

        self.tabel.column("id", width=40, anchor="center")
        self.tabel.column("judul", width=230)
        self.tabel.column("supplier", width=160)
        self.tabel.column("stok", width=60, anchor="center")

        self.tabel.pack(fill="both", expand=True, padx=15, pady=(0, 10))


if __name__ == "__main__":
    app = ctk.CTk()
    StokView(app).pack(fill="both", expand=True)
    app.mainloop()

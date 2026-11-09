import customtkinter as ctk
from tkinter import ttk


class SupplierView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # FRAME KIRI: FORM SUPPLIER
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            self.frame_kiri,
            text="Form Data Supplier",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        self.entry_nama = ctk.CTkEntry(self.frame_kiri, placeholder_text="Nama Supplier")
        self.entry_nama.pack(pady=10, padx=15, fill="x")

        self.entry_alamat = ctk.CTkEntry(self.frame_kiri, placeholder_text="Alamat")
        self.entry_alamat.pack(pady=10, padx=15, fill="x")

        self.entry_telepon = ctk.CTkEntry(self.frame_kiri, placeholder_text="Telepon")
        self.entry_telepon.pack(pady=10, padx=15, fill="x")

        self.btn_simpan = ctk.CTkButton(self.frame_kiri, text="Simpan Data", fg_color="green")
        self.btn_simpan.pack(pady=(15, 5), padx=15, fill="x")

        self.btn_ubah = ctk.CTkButton(self.frame_kiri, text="Ubah Data", fg_color="blue")
        self.btn_ubah.pack(pady=5, padx=15, fill="x")

        self.btn_hapus = ctk.CTkButton(self.frame_kiri, text="Hapus Data", fg_color="red")
        self.btn_hapus.pack(pady=5, padx=15, fill="x")

        self.btn_bersihkan = ctk.CTkButton(self.frame_kiri, text="Bersihkan Form", fg_color="gray")
        self.btn_bersihkan.pack(pady=5, padx=15, fill="x")

        # FRAME KANAN: TABEL SUPPLIER
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            self.frame_kanan,
            text="Daftar Supplier",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        kolom = ("id", "nama", "alamat", "telepon")
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=15)

        self.tabel.heading("id", text="ID")
        self.tabel.heading("nama", text="Nama Supplier")
        self.tabel.heading("alamat", text="Alamat")
        self.tabel.heading("telepon", text="Telepon")

        self.tabel.column("id", width=40, anchor="center")
        self.tabel.column("nama", width=180)
        self.tabel.column("alamat", width=220)
        self.tabel.column("telepon", width=110)

        self.tabel.pack(fill="both", expand=True, padx=15, pady=(0, 10))


if __name__ == "__main__":
    app = ctk.CTk()
    SupplierView(app).pack(fill="both", expand=True)
    app.mainloop()

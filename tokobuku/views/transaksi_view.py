import customtkinter as ctk
from tkinter import ttk


class TransaksiView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # FRAME KIRI: PILIH BUKU
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            self.frame_kiri,
            text="Transaksi Penjualan",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        ctk.CTkLabel(self.frame_kiri, text="Cari Buku (ketik judul / ID)").pack(padx=15, anchor="w")
        self.combo_buku = ctk.CTkComboBox(self.frame_kiri, values=[""])
        self.combo_buku.pack(pady=10, padx=15, fill="x")

        self.entry_jumlah = ctk.CTkEntry(self.frame_kiri, placeholder_text="Jumlah beli")
        self.entry_jumlah.pack(pady=10, padx=15, fill="x")

        self.btn_tambah = ctk.CTkButton(self.frame_kiri, text="Tambah ke Keranjang", fg_color="green")
        self.btn_tambah.pack(pady=(15, 5), padx=15, fill="x")

        self.btn_hapus_item = ctk.CTkButton(self.frame_kiri, text="Hapus Item Terpilih", fg_color="red")
        self.btn_hapus_item.pack(pady=5, padx=15, fill="x")

        # FRAME KANAN: KERANJANG
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            self.frame_kanan,
            text="Keranjang Belanja",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        kolom = ("id", "judul", "harga", "jumlah", "subtotal")
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=12)

        self.tabel.heading("id", text="ID")
        self.tabel.heading("judul", text="Judul Buku")
        self.tabel.heading("harga", text="Harga")
        self.tabel.heading("jumlah", text="Jumlah")
        self.tabel.heading("subtotal", text="Subtotal")

        self.tabel.column("id", width=40, anchor="center")
        self.tabel.column("judul", width=250)
        self.tabel.column("harga", width=90, anchor="e")
        self.tabel.column("jumlah", width=60, anchor="center")
        self.tabel.column("subtotal", width=100, anchor="e")

        self.tabel.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        # FRAME BAWAH: TOTAL DAN PEMBAYARAN
        self.frame_bawah = ctk.CTkFrame(self)
        self.frame_bawah.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        self.label_total = ctk.CTkLabel(
            self.frame_bawah,
            text="Total: Rp 0",
            font=("Arial", 16, "bold")
        )
        self.label_total.pack(side="left", padx=20, pady=10)

        self.btn_bayar = ctk.CTkButton(self.frame_bawah, text="Bayar & Cetak Struk", fg_color="blue")
        self.btn_bayar.pack(side="right", padx=15, pady=10)

        # Metode pembayaran: Tunai (kasir ketik nominal uang) atau Non Tunai (langsung struk)
        self.seg_metode = ctk.CTkSegmentedButton(self.frame_bawah, values=["Tunai", "Non Tunai"])
        self.seg_metode.set("Tunai")
        self.seg_metode.pack(side="right", padx=10, pady=10)

        self.entry_bayar = ctk.CTkEntry(self.frame_bawah, placeholder_text="Uang dibayar")
        self.entry_bayar.pack(side="right", padx=10, pady=10, before=self.seg_metode)


if __name__ == "__main__":
    app = ctk.CTk()
    TransaksiView(app).pack(fill="both", expand=True)
    app.mainloop()

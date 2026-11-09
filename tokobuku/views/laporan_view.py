import customtkinter as ctk
from tkinter import ttk


class LaporanView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(
            self,
            text="Laporan Transaksi",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        kolom = ("id", "tanggal", "kasir", "total", "bayar", "kembalian")
        self.tabel = ttk.Treeview(self, columns=kolom, show="headings", height=14)

        self.tabel.heading("id", text="No. Transaksi")
        self.tabel.heading("tanggal", text="Tanggal")
        self.tabel.heading("kasir", text="Kasir")
        self.tabel.heading("total", text="Total")
        self.tabel.heading("bayar", text="Bayar")
        self.tabel.heading("kembalian", text="Kembalian")

        self.tabel.column("id", width=90, anchor="center")
        self.tabel.column("tanggal", width=160)
        self.tabel.column("kasir", width=150)
        self.tabel.column("total", width=110, anchor="e")
        self.tabel.column("bayar", width=110, anchor="e")
        self.tabel.column("kembalian", width=110, anchor="e")

        self.tabel.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        self.frame_bawah = ctk.CTkFrame(self)
        self.frame_bawah.pack(fill="x", padx=15, pady=(0, 10))

        self.label_total = ctk.CTkLabel(
            self.frame_bawah,
            text="Total Pendapatan: Rp 0",
            font=("Arial", 14, "bold")
        )
        self.label_total.pack(side="left", padx=15, pady=10)

        self.btn_struk = ctk.CTkButton(self.frame_bawah, text="Cetak Struk", fg_color="blue")
        self.btn_struk.pack(side="right", padx=15, pady=10)


if __name__ == "__main__":
    app = ctk.CTk()
    LaporanView(app).pack(fill="both", expand=True)
    app.mainloop()

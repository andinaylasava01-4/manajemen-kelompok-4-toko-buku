import customtkinter as ctk


class PencarianBuku:
    """Menjadikan CTkComboBox sebagai kolom pencarian buku yang bisa diketik manual.

    - Ketik sebagian judul / ID buku, daftar pilihan otomatis tersaring.
    - Pilihan tetap bisa diambil dari daftar dropdown (klik panah).
    - Jika hanya satu buku yang cocok dengan teks yang diketik, buku itu langsung dipakai.
    """

    TIDAK_ADA = "(buku tidak ditemukan)"

    def __init__(self, combo):
        self.combo = combo
        self.semua = []
        self.label_hasil = ctk.CTkLabel(
            combo.master, text="", font=("Arial", 11), text_color="gray")
        self.label_hasil.pack(padx=15, anchor="w", after=combo)
        combo._entry.bind("<KeyRelease>", self._saat_ketik, add="+")

    def set_pilihan(self, pilihan):
        self.semua = list(pilihan)
        self.combo.configure(values=self.semua if self.semua else [""])
        self.label_hasil.configure(text="")

    def _cocok(self, teks):
        teks = teks.strip().lower()
        if not teks:
            return list(self.semua)
        return [p for p in self.semua if teks in p.lower()]

    def _saat_ketik(self, event=None):
        teks = self.combo.get()
        hasil = self._cocok(teks)
        self.combo.configure(values=hasil if hasil else [self.TIDAK_ADA])
        if not teks.strip():
            self.label_hasil.configure(text="")
        elif hasil:
            self.label_hasil.configure(text=f"{len(hasil)} buku cocok (klik panah untuk memilih)")
        else:
            self.label_hasil.configure(text="Buku tidak ditemukan")

    def ambil_id(self):
        """Kembalikan id_buku dari teks yang diketik/dipilih, atau None jika tidak jelas."""
        teks = self.combo.get().strip()
        if not teks or teks == self.TIDAK_ADA:
            return None

        # Pilihan persis dari dropdown: format "id - judul ..."
        if teks in self.semua:
            return int(teks.split(" - ")[0])

        # Hasil ketikan manual: harus tepat satu buku yang cocok
        hasil = self._cocok(teks)
        if len(hasil) == 1:
            return int(hasil[0].split(" - ")[0])
        return None

    def reset(self):
        self.combo.set("")
        self.combo.configure(values=self.semua if self.semua else [""])
        self.label_hasil.configure(text="")

class ComboBoxFilter:
    """Untuk kolom teks bebas (misal Kategori) yang tidak pakai id.

    Daftar pilihan ikut tersaring saat mengetik, tapi teks apa pun tetap
    boleh diketik bebas (termasuk membuat kategori baru).
    """

    def __init__(self, combo):
        self.combo = combo
        self.semua = []
        combo._entry.bind("<KeyRelease>", self._saat_ketik, add="+")

    def set_pilihan(self, pilihan):
        self.semua = list(pilihan)
        self.combo.configure(values=self.semua if self.semua else [""])

    def _saat_ketik(self, event=None):
        teks = self.combo.get().strip().lower()
        hasil = self.semua if not teks else [p for p in self.semua if teks in p.lower()]
        self.combo.configure(values=hasil if hasil else self.semua)

    def reset(self):
        self.combo.set("")
        self.combo.configure(values=self.semua if self.semua else [""])

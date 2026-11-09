import tkinter.messagebox as messagebox
from models.transaksi_model import TransaksiModel
from views.laporan_view import LaporanView
from controllers.struk_controller import StrukController, rupiah


class LaporanController:
    def __init__(self, parent, user_role):
        self.user_role = user_role
        self.model = TransaksiModel()
        self.view = LaporanView(parent)
        self.view.pack(fill="both", expand=True)

        self.view.btn_struk.configure(command=self.cetak_struk)

        # OTORISASI: hanya kasir yang boleh mencetak struk
        if self.user_role != "kasir":
            self.view.btn_struk.configure(state="disabled", text="Cetak Struk (Khusus Kasir)")

        self.refresh()

    def refresh(self):
        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data = self.model.get_all_transaksi()
        for t in data:
            self.view.tabel.insert("", "end", values=(
                t['id_transaksi'], t['tanggal'], t['kasir'],
                t['total'], t['bayar'], t['kembalian']))

        pendapatan = sum(t['total'] for t in data)
        self.view.label_total.configure(text=f"Total Pendapatan: {rupiah(pendapatan)}")

    def cetak_struk(self):
        pilihan = self.view.tabel.selection()
        if not pilihan:
            messagebox.showwarning("Peringatan", "Pilih transaksi pada tabel terlebih dahulu!")
            return

        id_transaksi = int(self.view.tabel.item(pilihan[0])["values"][0])
        transaksi = self.model.get_transaksi(id_transaksi)
        detail = self.model.get_detail(id_transaksi)
        StrukController.tampilkan(self.view.winfo_toplevel(), transaksi, detail)

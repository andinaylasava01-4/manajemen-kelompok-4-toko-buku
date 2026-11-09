from views.struk_view import StrukView


def rupiah(angka):
    return "Rp " + f"{int(angka):,}".replace(",", ".")


class StrukController:
    @staticmethod
    def buat_teks(transaksi, detail, metode=None):
        lebar = 36
        baris = [
            "TOKO BUKU".center(lebar),
            "=" * lebar,
            f"No    : {transaksi['id_transaksi']}",
            f"Tgl   : {transaksi['tanggal']}",
            f"Kasir : {transaksi['kasir']}",
            "-" * lebar,
        ]
        for item in detail:
            baris.append(item["judul"][:lebar])
            kiri = f"  {item['jumlah']} x {rupiah(item['harga'])}"
            baris.append(kiri.ljust(lebar - 14) + rupiah(item["subtotal"]).rjust(14))
        baris.append("-" * lebar)
        baris.append("TOTAL".ljust(lebar - 14) + rupiah(transaksi["total"]).rjust(14))
        if metode:
            baris.append("METODE".ljust(lebar - 14) + metode.rjust(14))
        baris.append("BAYAR".ljust(lebar - 14) + rupiah(transaksi["bayar"]).rjust(14))
        baris.append("KEMBALIAN".ljust(lebar - 14) + rupiah(transaksi["kembalian"]).rjust(14))
        baris.append("=" * lebar)
        baris.append("Terima kasih".center(lebar))
        return "\n".join(baris)

    @staticmethod
    def tampilkan(parent, transaksi, detail, metode=None):
        teks = StrukController.buat_teks(transaksi, detail, metode)
        return StrukView(parent, teks)

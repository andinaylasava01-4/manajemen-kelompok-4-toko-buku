import customtkinter as ctk


class StrukView(ctk.CTkToplevel):
    def __init__(self, parent, teks):
        super().__init__(parent)
        self.title("Struk Pembelian")
        self.geometry("380x500")

        self.textbox = ctk.CTkTextbox(self, font=("Courier New", 12))
        self.textbox.pack(fill="both", expand=True, padx=15, pady=15)
        self.textbox.insert("1.0", teks)
        self.textbox.configure(state="disabled")

        self.btn_tutup = ctk.CTkButton(self, text="Tutup", command=self.destroy)
        self.btn_tutup.pack(pady=(0, 15), padx=15, fill="x")

        # Pastikan jendela struk tampil di depan
        self.after(200, self.lift)

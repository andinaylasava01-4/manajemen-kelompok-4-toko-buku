import customtkinter as ctk


class MainView(ctk.CTk):
    def __init__(self, nama, role):
        super().__init__()
        self.title(f"Sistem Informasi Manajemen Toko Buku - {role.upper()}")
        self.geometry("1050x560")

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(10, 0), padx=15)

        ctk.CTkLabel(
            header,
            text=f"Login sebagai: {nama} ({role})",
            font=("Arial", 14, "bold")
        ).pack(side="left")

        self.btn_logout = ctk.CTkButton(header, text="Logout", width=90, fg_color="red")
        self.btn_logout.pack(side="right")

        # Menu berbentuk tab, isinya ditentukan oleh role pengguna
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

    def tambah_tab(self, nama_tab):
        return self.tabview.add(nama_tab)

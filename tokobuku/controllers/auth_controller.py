import tkinter.messagebox as messagebox
from models.akun_model import AkunModel
from views.login_view import LoginView
from controllers.main_controller import MainController


class AuthController:
    def __init__(self):
        self.logout = False  # True jika pengguna menekan tombol Logout
        self.model = AkunModel()
        self.view = LoginView()
        self.view.btn_login.configure(command=self.proses_login)

    def proses_login(self):
        username = self.view.entry_username.get()
        password = self.view.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password wajib diisi!")
            return

        user = self.model.autentikasi(username, password)

        if user:
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {user['nama']} ({user['role']})!")
            # tutup jendela Login
            self.view.destroy()
            # Buka jendela Utama dengan mengirimkan data pengguna (role menentukan menu)
            app_utama = MainController(user)
            app_utama.run()
            self.logout = app_utama.logout_diminta
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah!")

    def run(self):
        self.view.mainloop()

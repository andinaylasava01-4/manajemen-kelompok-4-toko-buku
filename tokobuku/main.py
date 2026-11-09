from controllers.auth_controller import AuthController


if __name__ == "__main__":
    # Setelah Logout, tampilkan kembali halaman Login
    while True:
        app = AuthController()
        app.run()
        if not app.logout:
            break

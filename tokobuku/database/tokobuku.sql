CREATE DATABASE IF NOT EXISTS tokobuku;
USE tokobuku;

-- Tabel akun: admin, kasir, dan pemilik (hak akses ditentukan oleh kolom role)
CREATE TABLE akun (
  id_akun INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(64) NOT NULL,
  nama VARCHAR(100) NOT NULL,
  role ENUM('admin','kasir','pemilik') NOT NULL
);

CREATE TABLE supplier (
  id_supplier INT AUTO_INCREMENT PRIMARY KEY,
  nama_supplier VARCHAR(100) NOT NULL,
  alamat VARCHAR(255) NOT NULL,
  telepon VARCHAR(20) NOT NULL
);

CREATE TABLE buku (
  id_buku INT AUTO_INCREMENT PRIMARY KEY,
  judul VARCHAR(200) NOT NULL,
  penulis VARCHAR(100) NOT NULL,
  kategori VARCHAR(50) NOT NULL,
  harga INT NOT NULL,
  stok INT NOT NULL DEFAULT 0,
  id_supplier INT NOT NULL,
  FOREIGN KEY (id_supplier) REFERENCES supplier(id_supplier)
);

CREATE TABLE transaksi (
  id_transaksi INT AUTO_INCREMENT PRIMARY KEY,
  tanggal DATETIME NOT NULL,
  id_akun INT NOT NULL,
  total INT NOT NULL,
  bayar INT NOT NULL,
  kembalian INT NOT NULL,
  FOREIGN KEY (id_akun) REFERENCES akun(id_akun)
);

CREATE TABLE detail_transaksi (
  id_detail INT AUTO_INCREMENT PRIMARY KEY,
  id_transaksi INT NOT NULL,
  id_buku INT NOT NULL,
  jumlah INT NOT NULL,
  harga INT NOT NULL,
  subtotal INT NOT NULL,
  FOREIGN KEY (id_transaksi) REFERENCES transaksi(id_transaksi) ON DELETE CASCADE,
  FOREIGN KEY (id_buku) REFERENCES buku(id_buku)
);

-- ===== DATA AWAL =====
INSERT INTO akun (username, password, nama, role) VALUES
('admin', SHA2('admin123', 256), 'Administrator', 'admin'),
('kasir', SHA2('kasir123', 256), 'Kasir Toko', 'kasir'),
('pemilik', SHA2('pemilik123', 256), 'Pemilik Toko', 'pemilik');

INSERT INTO supplier (nama_supplier, alamat, telepon) VALUES
('CV Pustaka Jaya', 'Jl. Merdeka 10, Palu', '0451123456'),
('PT Gramedia Distribusi', 'Jl. Sudirman 5, Makassar', '0411987654');

INSERT INTO buku (judul, penulis, kategori, harga, stok, id_supplier) VALUES
('Laskar Pelangi', 'Andrea Hirata', 'Novel', 89000, 20, 1),
('Bumi Manusia', 'Pramoedya A. Toer', 'Novel', 120000, 12, 1),
('Matematika SMA Kelas X', 'Tim Penulis', 'Pelajaran', 75000, 30, 2),
('Algoritma dan Pemrograman', 'Rinaldi Munir', 'Komputer', 135000, 4, 2),
('Belajar Python Dasar', 'Budi Raharjo', 'Komputer', 98000, 15, 2),
('Dongeng Nusantara', 'Tim Redaksi', 'Anak-anak', 55000, 8, 1);

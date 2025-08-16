#!/bin/bash

# Pastikan skrip dijalankan sebagai root
if [ "$EUID" -ne 0 ]; then
  echo "Harap jalankan skrip ini sebagai root (gunakan sudo)"
  exit
fi

echo ">>> 1. Memperbarui daftar paket..."
apt-get update

# Deteksi OS untuk paket SSG yang benar
if [ -f /etc/os-release ] && grep -q "ID=debian" /etc/os-release; then
  SSG_PACKAGE="ssg-debian"
  echo ">>> Terdeteksi Debian. Menggunakan paket ssg-debian."
else
  SSG_PACKAGE="ssg-ubuntu"
  echo ">>> Terdeteksi Ubuntu (atau turunan). Menggunakan paket ssg-ubuntu."
fi

echo ">>> 2. Menginstal dependensi sistem: Python3, Pip, dan Tools Keamanan..."
# Instal semua tool dan dependensi Python
DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip lynis rkhunter openscap-scanner "$SSG_PACKAGE"

echo ">>> 3. Menginstal pustaka Python yang dibutuhkan..."
pip3 install simple-term-menu

echo ">>> 4. Memberikan izin eksekusi pada skrip utama..."
chmod +x security_dashboard.py

echo -e "\n\n✅ Instalasi Selesai!"
echo "------------------------------------------"
echo "Untuk menjalankan aplikasi, gunakan perintah:"
echo "sudo ./security_dashboard.py"
echo "atau"
echo "sudo python3 security_dashboard.py"
echo "------------------------------------------"

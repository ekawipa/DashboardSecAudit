# 🛡️ Security Audit & System Info Dashboard (Advanced Edition)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Ubuntu%2FDebian-lightgrey.svg)
![Status](https://img.shields.io/badge/status-stable-success.svg)

> **All-in-One Terminal Dashboard** untuk mempercepat dan menyederhanakan tugas tim Blue Team, sysadmin, dan analis keamanan.  
> Menyediakan antarmuka menu tunggal untuk audit keamanan, pemeriksaan konfigurasi sistem, serta pemantauan jaringan pada distribusi **Ubuntu/Debian**.

---

## 📺 Demo / Preview


---

## 📌 Fitur Utama

### 🔍 Audit Keamanan Terpusat
- **Lynis** → Audit keamanan sistem secara menyeluruh  
- **Rkhunter** → Pindai rootkit, backdoor, exploit lokal  
- **OpenSCAP** → Pemindaian compliance (CIS Benchmarks, dsb.)

### 🖥️ Informasi Sistem Real-time
- **Jaringan**: port terbuka (`ss`), konfigurasi IP (`ip addr`), routing table, iptables  
- **Layanan**: status systemd services, firewall (UFW/Firewalld)  
- **Hardware & OS**: kernel, CPU, memory usage  
- **Konfigurasi Kritis**: SSHD audit, web service (Apache/Nginx) + modul/plugin aktif  

### 🤖 Fitur Cerdas
- ✅ **Auto-dependency check & install** (tool & Python libs)  
- 📝 **Logging session** → hasil audit tersimpan otomatis di `logs/` dengan timestamp  
- 📦 **SCAP content auto-detect** (SSG sesuai distro & versi)  
- 🖥️ **UI intuitif** berbasis terminal (navigasi keyboard)  

---

## 🚀 Instalasi & Penggunaan

### Metode 1: Instalasi via Skrip (Direkomendasikan)
```bash
git clone https://github.com/ekawipa/DashboardSecAudit.git
cd DashboardSecAudit
chmod +x install.sh
sudo ./install.sh

Metode 2: Eksekusi Langsung Skrip Python

wget https://raw.githubusercontent.com/ekawipa/security-dashboard/main/security_dashboard.py
chmod +x security_dashboard.py
sudo ./security_dashboard.py

Menjalankan Aplikasi

sudo ./security_dashboard.py

📝 Logging & Audit Trail

Setiap sesi akan otomatis membuat log di direktori logs/ dengan format:

logs/dashboard-session-2025-08-16_14-30-00.log

Log berisi:

    Perintah yang dieksekusi

    Output stdout & stderr

    Status (sukses/gagal)

📂 Struktur Repositori

.
├── security_dashboard.py   # Skrip utama aplikasi Python
├── install.sh              # Skrip instalasi otomatis dependensi
├── logs/                   # Direktori log (dibuat otomatis)
└── README.md               # Dokumentasi

🤝 Kontribusi

Kontribusi sangat terbuka 🙌

    Buat Issue untuk bug/fitur baru

    Ajukan Pull Request untuk perbaikan

📜 Lisensi

Proyek ini dilisensikan di bawah MIT License.
Author: Eka W. Prasetya (defsecOPS · @ekawprasetya)

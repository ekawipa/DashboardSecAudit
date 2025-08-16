Dashboard Audit Keamanan Terminal (Edisi Lanjutan)

Sebuah dashboard all-in-one berbasis terminal yang dirancang untuk mempercepat dan menyederhanakan tugas-tugas tim biru (Blue Team), administrator sistem, dan analis keamanan. Aplikasi ini menyediakan antarmuka menu tunggal untuk menjalankan audit keamanan, memeriksa konfigurasi sistem, dan memantau status jaringan pada sistem operasi berbasis Ubuntu/Debian.
Tampilan Aplikasi

Antarmuka menu telah diperluas untuk mencakup berbagai alat informasi dan diagnostik sistem.

┌──────────────────────────────────────────────────┐
│ ===== Security Audit & System Info Dashboard ===== │
├──────────────────────────────────────────────────┤
│ --- Audit Keamanan ---                           │
│ > Jalankan Lynis Audit                           │
│   Jalankan Rkhunter Scan                         │
│   Jalankan OpenSCAP Scan                         │
│ --- Informasi & Konfigurasi Sistem ---           │
│   Lihat Port yang Listening                      │
│   Lihat Service yang Berjalan                    │
│   Lihat Info Hardware & Kernel                   │
│   Periksa Status Firewall                        │
│   Lihat Konfigurasi Jaringan (ip addr)           │
│   Lihat Tabel Routing                            │
│   Lihat Aturan Iptables                          │
│   Periksa Konfigurasi SSHD                       │
│   Cek Web Service & Plugin                       │
│ ---                                              │
│   Keluar                                         │
└──────────────────────────────────────────────────┘


✨ Fitur Unggulan

Proyek ini telah berevolusi dari sekadar launcher menjadi toolkit yang lebih cerdas:
Audit Keamanan Terpusat

    Lynis: Jalankan audit pengerasan keamanan sistem secara menyeluruh.

    Rkhunter: Pindai sistem untuk mencari rootkit, backdoor, dan exploit lokal.

    OpenSCAP: Lakukan pemindaian kepatuhan (compliance) terhadap standar keamanan formal seperti CIS Benchmarks.

Informasi Sistem Real-time

    Jaringan: Lihat port yang terbuka (ss), konfigurasi IP, tabel routing, dan aturan iptables.

    Layanan (Services): Tampilkan semua layanan systemd yang aktif dan periksa status firewall (UFW atau Firewalld).

    Perangkat Keras & OS: Dapatkan informasi cepat mengenai Kernel, CPU, dan penggunaan memori.

    Konfigurasi Kritis: Audit konfigurasi efektif SSHD dan deteksi layanan web (Apache/Nginx) beserta modul yang sedang berjalan.

Fitur Cerdas

    ✅ Pemeriksaan & Instalasi Dependensi Otomatis: Skrip akan mendeteksi tool atau pustaka Python yang hilang dan menawarkan untuk menginstalnya secara otomatis saat pertama kali dijalankan.

    📝 Pencatatan Sesi (Logging): Setiap sesi dan output perintah penting secara otomatis dicatat ke dalam direktori logs/ dengan stempel waktu, menciptakan jejak audit (audit trail) yang berguna.

    🤖 Deteksi Konten SCAP Dinamis: Secara otomatis menemukan file konten SCAP Security Guide (SSG) yang relevan untuk distribusi (Ubuntu/Debian) dan versi Anda.

    🖥️ Antarmuka Intuitif: Menu yang bersih dan navigasi yang mudah menggunakan keyboard, membuat semua fitur dapat diakses dengan cepat.

🚀 Instalasi dan Penggunaan

Anda bisa memilih salah satu dari dua metode instalasi berikut.
Metode 1: Menggunakan Skrip Instalasi (Disarankan untuk Awal)

Metode ini akan menyiapkan semuanya untuk Anda, cocok untuk sistem yang bersih.

    Clone Repositori

    git clone [URL_REPOSITORI_ANDA_DI_SINI]
    cd [NAMA_DIREKTORI_REPOSITORI]


    Jalankan Skrip Instalasi
    Skrip ini akan menginstal semua tool sistem dan pustaka Python yang dibutuhkan.

    chmod +x install.sh
    sudo ./install.sh


Metode 2: Eksekusi Langsung Skrip Python

Berkat fitur pengecekan dependensi internal, Anda juga bisa langsung menjalankan skrip Python.

    Unduh Skrip Utama
    Unduh hanya file security_dashboard.py.

    Berikan Izin Eksekusi

    chmod +x security_dashboard.py


    Jalankan Skrip
    Saat dijalankan pertama kali, skrip akan memeriksa dependensi yang hilang dan meminta izin Anda untuk menginstalnya.

    sudo ./security_dashboard.py


Menjalankan Aplikasi

Setelah instalasi, jalankan dashboard kapan saja dengan perintah:

sudo ./security_dashboard.py


📝 Pencatatan (Logging)

Fitur ini sangat penting untuk analisis pasca-audit. Setiap kali Anda menjalankan dashboard, sebuah file log baru akan dibuat di dalam direktori logs/.

Contoh nama file: logs/dashboard-session-2025-08-16_14-30-00.log

File ini berisi:

    Perintah yang dieksekusi.

    Output standar (stdout) dan error standar (stderr) dari perintah yang penting.

    Pesan status (sukses atau gagal).

Ini memungkinkan Anda untuk meninjau kembali hasil pemindaian atau diagnosis tanpa harus menjalankan ulang perintahnya.
Struktur File Repositori

.
├── security_dashboard.py   # Skrip utama aplikasi Python
├── install.sh              # Skrip untuk instalasi otomatis semua dependensi
├── logs/                   # Direktori (dibuat otomatis) untuk menyimpan file log sesi
└── README.md               # File dokumentasi ini


Kontribusi

Kontribusi, laporan bug, atau permintaan fitur sangat kami hargai! Silakan buat Issue baru di repositori GitHub ini untuk memulai diskusi.
Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT.

Author : Eka W. Prasetya (defsecOPS @ekawprasetya)

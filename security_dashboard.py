#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import re
import shutil
import subprocess
from datetime import datetime

# Coba impor, tapi jangan gagalkan skrip jika belum diinstal.
# Pemeriksaan dependensi akan menanganinya.
try:
    from simple_term_menu import TerminalMenu
except ImportError:
    pass # Akan ditangani oleh check_and_install_dependencies

def check_privileges():
    """Memeriksa apakah skrip dijalankan sebagai root."""
    if os.geteuid() != 0:
        print("❌ Error: Skrip ini harus dijalankan dengan hak akses root (gunakan 'sudo').")
        sys.exit(1)

def check_and_install_dependencies():
    """Memeriksa semua dependensi (sistem dan Python) dan menawarkan untuk menginstalnya."""
    print("🔎 Memeriksa semua dependensi...")
    
    # --- Paket Sistem ---
    required_executables = { "lynis": "lynis", "rkhunter": "rkhunter", "oscap": "openscap-scanner" }
    ssg_content_path = "/usr/share/xml/scap/ssg/content/"
    ssg_package = "ssg-ubuntu"
    try:
        with open("/etc/os-release") as f:
            if "ID=debian" in f.read():
                ssg_package = "ssg-debian"
    except FileNotFoundError:
        print("⚠️  Peringatan: Tidak dapat mendeteksi distribusi Linux. Mengasumsikan Ubuntu untuk paket SSG.")

    missing_apt_packages = []
    for executable, package in required_executables.items():
        if not shutil.which(executable):
            print(f"    - ❌ Tool '{executable}' tidak ditemukan (paket: {package}).")
            missing_apt_packages.append(package)

    if not os.path.isdir(ssg_content_path):
        print(f"    - ❌ Konten OpenSCAP SSG tidak ditemukan (paket: {ssg_package}).")
        if ssg_package not in missing_apt_packages:
            missing_apt_packages.append(ssg_package)

    # --- Paket Python ---
    missing_pip_packages = []
    try:
        from simple_term_menu import TerminalMenu
    except ImportError:
        print("    - ❌ Pustaka Python 'simple-term-menu' tidak ditemukan.")
        missing_pip_packages.append("simple-term-menu")
        # Kita akan membutuhkan pip untuk menginstalnya
        if not shutil.which("pip3"):
             if "python3-pip" not in missing_apt_packages:
                missing_apt_packages.append("python3-pip")

    # --- Instalasi ---
    if not missing_apt_packages and not missing_pip_packages:
        print("✅ Semua dependensi sudah terinstal.")
        return

    # Bangun pesan yang komprehensif
    install_prompt = "\nBeberapa dependensi tidak ditemukan. Apakah Anda ingin menginstalnya?\n"
    if missing_apt_packages:
        install_prompt += f"  - Paket sistem (via apt): {', '.join(missing_apt_packages)}\n"
    if missing_pip_packages:
        install_prompt += f"  - Pustaka Python (via pip): {', '.join(missing_pip_packages)}\n"
    
    answer = input(f"{install_prompt} [Y/n] ").lower().strip()

    if answer in ["y", "yes", ""]:
        print("\n🚀 Memulai instalasi... (Ini mungkin memakan waktu beberapa saat)")
        
        # Instal paket apt terlebih dahulu
        if missing_apt_packages:
            run_command(["apt-get", "update"], "Pembaruan Daftar Paket", capture=True)
            run_command(["apt-get", "install", "-y"] + missing_apt_packages, "Instalasi Dependensi Sistem", capture=True)
        
        # Instal paket pip
        if missing_pip_packages:
            run_command(["pip3", "install"] + missing_pip_packages, "Instalasi Pustaka Python", capture=True)
            
        print("\n✅ Instalasi dependensi berhasil! Silakan jalankan kembali dashboard untuk menerapkan perubahan.")
        sys.exit(0)  # Keluar dengan kode sukses
    else:
        print("\n❌ Instalasi dibatalkan. Skrip tidak dapat melanjutkan.")
        sys.exit(1)  # Keluar dengan kode error

def setup_logger():
    """Mengatur logger untuk menyimpan output ke file dengan stempel waktu."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"dashboard-session-{timestamp}.log")

    logger = logging.getLogger("dashboard_logger")
    logger.setLevel(logging.INFO)

    # Mencegah penambahan handler ganda jika fungsi dipanggil lagi
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    print(f"ℹ️  Sesi ini akan dicatat ke dalam file: {log_file}")
    return logger

def run_command(command, title, capture=False, logger=None):
    """Fungsi generik untuk menjalankan perintah, menampilkan output, mencatat, dan mengembalikan proses."""
    if logger:
        logger.info(f"Executing: {title} | Command: {' '.join(command)}")

    try:
        print(f"\n🚀 Menjalankan {title}...")
        print("-" * 40)
        
        if capture:
            # Jalankan, tangkap output, dan lempar exception jika gagal.
            process = subprocess.run(
                command, capture_output=True, text=True, check=True, 
                encoding='utf-8', errors='ignore'
            )
            print("-" * 40)
            print(f"✅ {title} selesai dengan sukses.")
            if logger:
                logger.info(f"SUCCESS: '{title}' finished with exit code 0.")
                if process.stdout:
                    logger.info(f"STDOUT for '{title}':\n{process.stdout.strip()}")
                if process.stderr:
                    logger.warning(f"STDERR for '{title}':\n{process.stderr.strip()}")
            return process
        else:
            # Jalankan secara interaktif, periksa return code secara manual.
            process = subprocess.run(command, check=False)
            print("-" * 40)
            if process.returncode == 0:
                print(f"✅ {title} selesai dengan sukses.")
                if logger:
                    logger.info(f"SUCCESS: '{title}' finished with exit code 0.")
            else:
                print(f"⚠️  {title} selesai dengan kode error: {process.returncode}.")
                if logger:
                    logger.error(f"FAILURE: '{title}' finished with exit code {process.returncode}.")
            return process

    except FileNotFoundError:
        message = f"Error: Perintah '{command[0]}' tidak ditemukan. Pastikan tool sudah terinstal."
        print(f"❌ {message}")
        if logger:
            logger.error(message)
    except (subprocess.CalledProcessError, Exception) as e:
        message = f"Error saat menjalankan '{title}': {e}"
        print(f"❌ {message}")
        if logger:
            logger.error(message, exc_info=True)
    return None

def run_lynis(logger):
    """Menjalankan audit sistem dengan Lynis."""
    log_file = "/var/log/lynis-dashboard-audit.log"
    # Menjalankan audit untuk semua kategori (-Q agar tidak menunggu interaksi user)
    # --logfile untuk menyimpan output ke file untuk review nanti
    command = ["lynis", "audit", "system", "-Q", "--logfile", log_file]
    
    run_command(command, "Lynis System Audit", logger=logger)
    
    print(f"\n💡 Tips: Hasil audit lengkap juga disimpan di {log_file}")
    input("\nTekan Enter untuk kembali ke menu...")


def run_rkhunter(logger):
    """Menjalankan pemindaian dengan Rkhunter."""
    # --check: memulai pemindaian, --skip-keypress: otomatis lanjut tanpa perlu menekan enter
    command = ["rkhunter", "--check", "--sk"]
    run_command(command, "Rkhunter Scan", logger=logger)
    
    print("\n💡 Tips: Untuk update definisi Rkhunter, jalankan 'sudo rkhunter --update'")
    input("\nTekan Enter untuk kembali ke menu...")

def find_scap_content_file():
    """Mencari file konten SCAP SSG yang relevan secara dinamis."""
    base_path = "/usr/share/xml/scap/ssg/content/"
    if not os.path.isdir(base_path):
        return None

    distro = 'ubuntu'  # Default
    version = ''
    try:
        with open("/etc/os-release") as f:
            content = f.read()
            distro_match = re.search(r'^ID=([a-zA-Z]*)', content, re.M)
            version_match = re.search(r'^VERSION_ID="?([0-9]+)', content, re.M)
            if distro_match:
                distro = distro_match.group(1)
            if version_match:
                version = version_match.group(1)
    except (FileNotFoundError, AttributeError):
        pass  # Gunakan default jika file tidak ada atau tidak bisa di-parse

    # 1. Coba cari file yang paling spesifik (e.g., ssg-ubuntu2204-ds.xml)
    specific_file = os.path.join(base_path, f"ssg-{distro}{version}-ds.xml")
    if os.path.exists(specific_file):
        return specific_file

    # 2. Jika tidak ada, cari file generik yang cocok dengan distro (e.g., ssg-ubuntu-ds.xml)
    try:
        for filename in os.listdir(base_path):
            if filename.startswith(f"ssg-{distro}") and filename.endswith("-ds.xml"):
                return os.path.join(base_path, filename)
    except FileNotFoundError:
        return None

    return None  # Tidak ada file yang ditemukan

def run_openscap(logger):
    """Menyediakan submenu untuk memilih profil OpenSCAP."""
    scap_content_file = find_scap_content_file()

    if not scap_content_file:
        print(f"❌ Error: File konten OpenSCAP tidak ditemukan di /usr/share/xml/scap/ssg/content/")
        print("Pastikan paket 'openscap-scanner' dan 'ssg-debian' atau 'ssg-ubuntu' sudah terinstal.")
        input("\nTekan Enter untuk kembali ke menu...")
        if logger:
            logger.error("OpenSCAP content file not found.")
        return
    
    # Contoh profil yang umum digunakan. Anda bisa menambahkan profil lain dari file XML di atas.
    profiles = {
        "CIS Benchmark Level 1 (Server)": "xccdf_org.ssgproject.content_profile_cis_level1_server",
        "CIS Benchmark Level 2 (Server)": "xccdf_org.ssgproject.content_profile_cis_level2_server",
        "Standard Security Profile for Ubuntu": "xccdf_org.ssgproject.content_profile_standard"
    }

    print(f"ℹ️  Menggunakan file konten SCAP: {os.path.basename(scap_content_file)}")
    
    terminal_menu = TerminalMenu(
        profiles.keys(),
        title="Pilih profil OpenSCAP untuk pemindaian:",
        menu_cursor_style=("fg_cyan", "bold"),
    )
    
    chosen_index = terminal_menu.show()
    
    if chosen_index is not None:
        profile_name = list(profiles.keys())[chosen_index]
        profile_id = profiles[profile_name]
        
        print(f"\nAnda memilih: {profile_name}")
        output_html = f"report-{profile_id}.html"
        
        # Perintah oscap
        command = [
            "oscap", "xccdf", "eval",
            "--profile", profile_id,
            "--report", output_html,
            scap_content_file
        ]
        
        run_command(command, f"OpenSCAP Scan ({profile_name})", logger=logger)
        print(f"\n📄 Laporan HTML telah disimpan di: {os.getcwd()}/{output_html}")
        input("\nTekan Enter untuk kembali ke menu...")

def show_listening_ports(logger):
    """Menampilkan port yang sedang listening (TCP/UDP)."""
    # ss lebih modern dari netstat. -t(tcp) u(udp) l(listen) n(numeric) p(processes)
    command = ["ss", "-tulnp"]
    run_command(command, "Port yang Sedang Listening", logger=logger)
    input("\nTekan Enter untuk kembali ke menu...")

def show_running_services(logger):
    """Menampilkan semua service yang sedang berjalan via systemd."""
    command = ["systemctl", "list-units", "--type=service", "--state=running", "--no-pager"]
    run_command(command, "Service yang Sedang Berjalan", logger=logger)
    input("\nTekan Enter untuk kembali ke menu...")

def show_system_hardware_info(logger):
    """Menampilkan informasi kernel, CPU, dan memori."""
    print("\nMenampilkan informasi sistem...")
    run_command(["uname", "-a"], "Informasi Kernel & OS", logger=logger)
    run_command(["lscpu"], "Informasi CPU", logger=logger)
    run_command(["free", "-h"], "Informasi Memori", logger=logger)
    input("\nTekan Enter untuk kembali ke menu...")

def show_firewall_status(logger):
    """Memeriksa dan menampilkan status firewall (UFW atau Firewalld)."""
    if shutil.which("ufw"):
        command = ["ufw", "status", "verbose"]
        run_command(command, "Status Firewall (UFW)", logger=logger)
    elif shutil.which("firewall-cmd"):
        print("Mendeteksi Firewalld. Memeriksa status service...")
        run_command(["systemctl", "status", "firewalld", "--no-pager"], "Status Service Firewalld", logger=logger)
        command = ["firewall-cmd", "--list-all"]
        run_command(command, "Konfigurasi Firewalld", logger=logger)
    else:
        print("\nℹ️ Tidak ada UFW atau Firewalld yang terdeteksi di sistem ini.")
        if logger: logger.info("No UFW or Firewalld detected.")
    input("\nTekan Enter untuk kembali ke menu...")

def show_network_config(logger):
    """Menampilkan konfigurasi semua interface jaringan."""
    command = ["ip", "addr"]
    run_command(command, "Konfigurasi Interface Jaringan", logger=logger)
    input("\nTekan Enter untuk kembali ke menu...")

def show_routing_table(logger):
    """Menampilkan tabel routing sistem."""
    command = ["ip", "route"]
    run_command(command, "Tabel Routing", logger=logger)
    input("\nTekan Enter untuk kembali ke menu...")

def show_iptables_rules(logger):
    """Menampilkan ruleset iptables (filter table)."""
    command = ["iptables", "-L", "-n", "-v"]
    run_command(command, "Aturan Iptables (Filter Table)", logger=logger)
    input("\nTekan Enter untuk kembali ke menu...")

def show_sshd_config(logger):
    """Menampilkan konfigurasi SSHD yang efektif."""
    # Menggunakan sshd -T lebih baik karena menampilkan konfigurasi final setelah semua include diproses
    # Kita capture outputnya agar bisa ditampilkan di layar dan juga dicatat di log.
    command = ["sshd", "-T"]
    process = run_command(command, "Konfigurasi Efektif SSHD", capture=True, logger=logger)
    if process and process.stdout:
        print("--- Konfigurasi Ditemukan ---")
        print(process.stdout.strip())
        print("--------------------------")
    print("\n💡 Tips: Periksa parameter seperti 'PermitRootLogin', 'PasswordAuthentication', dan 'X11Forwarding'.")
    input("\nTekan Enter untuk kembali ke menu...")

def show_web_services_info(logger):
    """Mendeteksi web server yang berjalan dan menampilkan modul/plugin yang relevan."""
    print("\n🔎 Mencari web service yang aktif...")
    
    web_servers = {
        # service_name: (executable_for_modules, module_command)
        "apache2": ("apache2ctl", ["apache2ctl", "-M"]),
        "nginx": ("nginx", ["nginx", "-V"]), # -V prints to stderr
        "httpd": ("httpd", ["httpd", "-M"]), # For RHEL/CentOS family
    }

    found_one = False
    # Jalankan ss sekali untuk mendapatkan semua info port
    try:
        ss_proc = subprocess.run(["ss", "-tlpn"], capture_output=True, text=True, check=True)
        if logger: logger.info(f"STDOUT for 'ss -tlpn':\n{ss_proc.stdout.strip()}")
        ss_output_lines = ss_proc.stdout.strip().split('\n')
    except (subprocess.CalledProcessError, FileNotFoundError):
        ss_output_lines = None
        print("⚠️  Peringatan: Tidak dapat menjalankan 'ss' untuk memeriksa port.")

    for service, (executable, module_cmd) in web_servers.items():
        is_active_proc = subprocess.run(["systemctl", "is-active", "--quiet", service], capture_output=True)
        
        if is_active_proc.returncode == 0: # 0 berarti aktif
            if not found_one:
                print("-" * 50)
            found_one = True
            if logger:
                logger.info(f"Active web service detected: {service}")
            
            print(f"✅ Web service '{service}' terdeteksi aktif.")
            
            # Tampilkan modul/konfigurasi
            if shutil.which(executable):
                print(f"\n  -- Modul/Konfigurasi untuk {service} --")
                proc = subprocess.run(module_cmd, capture_output=True, text=True)
                output = proc.stdout if proc.stdout else proc.stderr
                if logger:
                    logger.info(f"Module/Config output for '{service}':\n{output.strip()}")
                # Beri indentasi pada output untuk kejelasan
                for line in output.strip().split('\n'):
                    print(f"    {line}")
            
            # Tampilkan port yang digunakan oleh service ini
            if ss_output_lines:
                print(f"\n  -- Port yang digunakan oleh '{service}' --")
                header = ss_output_lines[0]
                matched_lines = [line for line in ss_output_lines[1:] if f'"{service}"' in line]
                if matched_lines:
                    print(f"    {header}")
                    for line in matched_lines:
                        print(f"    {line}")
            print("-" * 50)

    if not found_one:
        print("\nℹ️ Tidak ada web service umum (Apache, Nginx, dll.) yang terdeteksi aktif.")
        if logger:
            logger.info("No common web services (Apache, Nginx) found active.")

    input("\nTekan Enter untuk kembali ke menu...")

def main():
    """Fungsi utama untuk menampilkan menu."""
    check_privileges()
    # Logger di-setup setelah dependensi diperiksa, karena instalasi tidak perlu di-log
    check_and_install_dependencies()
    logger = setup_logger()
    logger.info("Dashboard session started.")

    main_menu_title = "===== Security Audit & System Info Dashboard ====="
    
    # Definisikan semua aksi menu dalam satu struktur data untuk kemudahan pengelolaan
    menu_actions = [
        ("--- Audit Keamanan ---", None),
        ("Jalankan Lynis Audit", lambda: run_lynis(logger)),
        ("Jalankan Rkhunter Scan", lambda: run_rkhunter(logger)),
        ("Jalankan OpenSCAP Scan", lambda: run_openscap(logger)),
        ("--- Informasi & Konfigurasi Sistem ---", None),
        ("Lihat Port yang Listening", lambda: show_listening_ports(logger)),
        ("Lihat Service yang Berjalan", lambda: show_running_services(logger)),
        ("Lihat Info Hardware & Kernel", lambda: show_system_hardware_info(logger)),
        ("Periksa Status Firewall", lambda: show_firewall_status(logger)),
        ("Lihat Konfigurasi Jaringan (ip addr)", lambda: show_network_config(logger)),
        ("Lihat Tabel Routing", lambda: show_routing_table(logger)),
        ("Lihat Aturan Iptables", lambda: show_iptables_rules(logger)),
        ("Periksa Konfigurasi SSHD", lambda: show_sshd_config(logger)),
        ("Cek Web Service & Plugin", lambda: show_web_services_info(logger)),
        ("---", None),
        ("Keluar", "exit")
    ]
    
    # Ekstrak nama item untuk ditampilkan di menu
    main_menu_items = [item[0] for item in menu_actions]
    
    main_menu = TerminalMenu(
        main_menu_items,
        title=main_menu_title,
        menu_cursor_style=("fg_green", "bold"),
        menu_highlight_style=("bg_green", "fg_black"),
        cycle_cursor=True
    )

    while True:
        # Membersihkan layar setiap kali menu ditampilkan
        os.system('cls' if os.name == 'nt' else 'clear')
        chosen_menu_index = main_menu.show()

        if chosen_menu_index is None:
            # User menekan Esc atau q, anggap sebagai keluar
            break

        # Dapatkan aksi yang sesuai dari struktur data
        action = menu_actions[chosen_menu_index][1]

        if action == "exit":
            break
        elif action is not None:
            action()
        # Jika action adalah None (pemisah), loop akan berlanjut dan menu ditampilkan lagi

    logger.info("Dashboard session ended.")
    print("👋 Terima kasih telah menggunakan dashboard ini. Sampai jumpa!")
    sys.exit(0)


if __name__ == "__main__":
    main()
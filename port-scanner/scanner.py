import socket
import concurrent.futures
import argparse
import sys
from datetime import datetime
from banner_grabber import grab_banner
from os_detector import detect_os_by_ttl

# Renk kodları
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Yaygın port isimleri
PORT_NAMES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 27017: "MongoDB"
}

def banner():
    print(f"""
{CYAN}╔═══════════════════════════════════════╗
║         PORT SCANNER v2.0 Pro         ║
║   github.com/mehmeteminyilmaz         ║
╚═══════════════════════════════════════╝{RESET}
""")

def scan_port(host: str, port: int, timeout: float = 1.0, do_banner: bool = False):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        is_open = (result == 0)
        banner_text = ""
        if is_open and do_banner:
            banner_text = grab_banner(host, port, timeout=1.5)

        return port, is_open, banner_text
    except Exception:
        return port, False, ""

def get_service(port: int) -> str:
    return PORT_NAMES.get(port, "Bilinmeyen Servis")

def scan_target(host: str, start_port: int, end_port: int, threads: int = 100, do_banner: bool = False, do_os: bool = False):
    banner()
    
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"{RED}[!] Host bulunamadı: {host}{RESET}")
        sys.exit(1)

    print(f"{YELLOW}[*] Hedef        : {host} ({ip})")
    print(f"[*] Port Aralığı : {start_port} - {end_port}")
    print(f"[*] İş Parçacığı : {threads}")
    print(f"[*] Başlangıç    : {datetime.now().strftime('%H:%M:%S')}{RESET}")
    
    if do_os:
        print(f"{CYAN}[*] İşletim Sistemi Analizi yapılıyor...{RESET}")
        os_info = detect_os_by_ttl(ip)
        print(f"{CYAN}[+] Tahmini OS   : {os_info['os_family']} (TTL: {os_info['ttl']}){RESET}")
        
    print("-" * 55)

    open_ports = []
    ports = range(start_port, end_port + 1)

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, ip, port, 1.0, do_banner): port for port in ports}
        for future in concurrent.futures.as_completed(futures):
            port, is_open, banner_info = future.result()
            if is_open:
                service = get_service(port)
                open_ports.append({"port": port, "service": service, "banner": banner_info})
                banner_str = f" → Banner: {banner_info}" if banner_info else ""
                print(f"{GREEN}[+] Port {port:5d}  AÇIK  →  {service}{banner_str}{RESET}")

    print("-" * 55)
    if open_ports:
        print(f"{GREEN}[✓] {len(open_ports)} açık port bulundu.{RESET}")
    else:
        print(f"{RED}[✗] Açık port bulunamadı.{RESET}")
    
    print(f"{YELLOW}[*] Bitiş: {datetime.now().strftime('%H:%M:%S')}{RESET}")
    return open_ports

def main():
    parser = argparse.ArgumentParser(
        description="Port Scanner v2.0 Pro — Siber Güvenlik Aracı",
        epilog="Örnek: python scanner.py scanme.nmap.org -s 1 -e 100 -b -o"
    )
    parser.add_argument("host", help="Hedef IP veya domain (örn: scanme.nmap.org)")
    parser.add_argument("-s", "--start", type=int, default=1, help="Başlangıç portu (varsayılan: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="Bitiş portu (varsayılan: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Thread sayısı (varsayılan: 100)")
    parser.add_argument("-b", "--banner", action="store_true", help="Servis banner yakalama (Banner Grabbing)")
    parser.add_argument("-o", "--os", action="store_true", help="İşletim sistemi tespiti (TTL Tabanlı OS Fingerprinting)")
    
    args = parser.parse_args()
    scan_target(args.host, args.start, args.end, args.threads, args.banner, args.os)

if __name__ == "__main__":
    main()

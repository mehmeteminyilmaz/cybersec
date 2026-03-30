import socket
import concurrent.futures
import argparse
import sys
from datetime import datetime

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
║         PORT SCANNER v1.0             ║
║   github.com/mehmeteminyilmaz         ║
╚═══════════════════════════════════════╝{RESET}
""")

def scan_port(host, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return port, result == 0
    except:
        return port, False

def get_service(port):
    return PORT_NAMES.get(port, "Unknown")

def scan_target(host, start_port, end_port, threads=100):
    banner()
    
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"{RED}[!] Host bulunamadı: {host}{RESET}")
        sys.exit(1)

    print(f"{YELLOW}[*] Hedef    : {host} ({ip})")
    print(f"[*] Port Aralığı : {start_port} - {end_port}")
    print(f"[*] Başlangıç  : {datetime.now().strftime('%H:%M:%S')}{RESET}")
    print("-" * 45)

    open_ports = []
    ports = range(start_port, end_port + 1)

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in ports}
        for future in concurrent.futures.as_completed(futures):
            port, is_open = future.result()
            if is_open:
                service = get_service(port)
                open_ports.append(port)
                print(f"{GREEN}[+] Port {port:5d}  AÇIK  →  {service}{RESET}")

    print("-" * 45)
    if open_ports:
        print(f"{GREEN}[✓] {len(open_ports)} açık port bulundu.{RESET}")
    else:
        print(f"{RED}[✗] Açık port bulunamadı.{RESET}")
    
    print(f"{YELLOW}[*] Bitiş: {datetime.now().strftime('%H:%M:%S')}{RESET}")

def main():
    parser = argparse.ArgumentParser(
        description="Port Scanner — Siber Güvenlik Aracı",
        epilog="Örnek: python scanner.py google.com -s 1 -e 1000"
    )
    parser.add_argument("host", help="Hedef IP veya domain (örn: scanme.nmap.org)")
    parser.add_argument("-s", "--start", type=int, default=1, help="Başlangıç portu (varsayılan: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="Bitiş portu (varsayılan: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Thread sayısı (varsayılan: 100)")
    
    args = parser.parse_args()
    scan_target(args.host, args.start, args.end, args.threads)

if __name__ == "__main__":
    main()

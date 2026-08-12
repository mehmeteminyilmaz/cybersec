from flask import Flask, render_template, request, jsonify
import socket
import concurrent.futures
from datetime import datetime
import sys
import os

# Port Scanner modülünü sys.path'e ekleyelim
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'port-scanner')))
try:
    from banner_grabber import grab_banner
    from os_detector import detect_os_by_ttl
except ImportError:
    def grab_banner(ip, port, timeout=1): return "Banner yok"
    def detect_os_by_ttl(ip): return {"os_family": "Bilinmeyen", "ttl": None}

app = Flask(__name__)

# --- CONFIG & CONSTANTS ---
PORT_NAMES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 27017: "MongoDB"
}

# --- HELPERS ---
def scan_port(host, port, timeout=1, do_banner=True):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        is_open = (result == 0)
        banner = ""
        if is_open and do_banner:
            banner = grab_banner(host, port, timeout=1.0)
            
        return port, is_open, banner
    except:
        return port, False, ""

def get_service(port):
    return PORT_NAMES.get(port, "Bilinmeyen Servis")

# --- ROUTES ---
@app.route('/')
def index():
    return render_template('index.html', active_page='dashboard')

@app.route('/port-scanner')
def port_scanner():
    return render_template('index.html', active_page='port-scanner')

# --- API ENDPOINTS ---
@app.route('/api/scan', methods=['POST'])
def api_scan():
    data = request.json or {}
    target = data.get('target')
    start_port = int(data.get('start_port', 1))
    end_port = int(data.get('end_port', 1024))
    threads = int(data.get('threads', 100))
    do_banner = bool(data.get('banner', True))
    do_os = bool(data.get('os_detect', True))

    if not target:
        return jsonify({"error": "Hedef belirtilmelidir."}), 400

    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        return jsonify({"error": "Sunucu (Host) bulunamadı."}), 404

    os_info = detect_os_by_ttl(ip) if do_os else {"os_family": "Bilinmiyor", "ttl": None}

    open_ports = []
    ports = range(start_port, end_port + 1)

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, ip, port, 1.0, do_banner): port for port in ports}
        for future in concurrent.futures.as_completed(futures):
            port, is_open, banner_info = future.result()
            if is_open:
                service = get_service(port)
                open_ports.append({
                    "port": port,
                    "service": service,
                    "status": "OPEN",
                    "banner": banner_info
                })

    open_ports.sort(key=lambda x: x['port'])

    return jsonify({
        "target": target,
        "ip": ip,
        "os_info": os_info,
        "count": len(open_ports),
        "results": open_ports,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

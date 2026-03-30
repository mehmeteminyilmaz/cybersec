from flask import Flask, render_template, request, jsonify
import socket
import concurrent.futures
from datetime import datetime

app = Flask(__name__)

# Yaygın port isimleri
PORT_NAMES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 27017: "MongoDB"
}

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
    return PORT_NAMES.get(port, "Unknown Service")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    target = data.get('target')
    start_port = int(data.get('start_port', 1))
    end_port = int(data.get('end_port', 1024))
    threads = int(data.get('threads', 100))

    if not target:
        return jsonify({"error": "Hedef IP/Domain girilmelidir."}), 400

    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        return jsonify({"error": "Host bulunamadı."}), 404

    open_ports = []
    ports = range(start_port, end_port + 1)

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in ports}
        for future in concurrent.futures.as_completed(futures):
            port, is_open = future.result()
            if is_open:
                service = get_service(port)
                open_ports.append({
                    "port": port,
                    "service": service,
                    "status": "OPEN"
                })

    # Sonuçları port numarasına göre sırala
    open_ports.sort(key=lambda x: x['port'])

    return jsonify({
        "target": target,
        "ip": ip,
        "count": len(open_ports),
        "results": open_ports,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

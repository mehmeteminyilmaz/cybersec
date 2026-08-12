import socket

def grab_banner(ip: str, port: int, timeout: float = 2.0) -> str:
    """
    Hedef IP ve port üzerindeki servisin sunduğu karşılama metnini (banner) yakalar.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        
        # HTTP portu ise basit bir GET isteği gönderelim
        if port in [80, 8080, 8443]:
            sock.send(b"HEAD / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
        elif port == 443:
            sock.close()
            return "SSL/TLS Encrypted"
        else:
            # Genellikle FTP, SSH, SMTP otomatik karşılama mesajı gönderir
            pass

        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        sock.close()
        return banner if banner else "Banner yok"
    except Exception as e:
        return f"Banner alınamadı ({str(e)})"

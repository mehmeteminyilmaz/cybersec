import subprocess
import re
import sys

def detect_os_by_ttl(ip: str) -> dict:
    """
    Hedef IP adresine ICMP ping atarak TTL (Time to Live) değerine göre tahmini İşletim Sistemi tespiti yapar.
    - Linux / Unix / Android / macOS: TTL ~ 64
    - Windows: TTL ~ 128
    - Cisco / Ağ Cihazları: TTL ~ 255
    """
    param = '-n' if sys.platform.startswith('win') else '-c'
    command = ['ping', param, '1', ip]

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True, timeout=3)
        ttl_match = re.search(r'ttl[=\s](\d+)', output, re.IGNORECASE)
        
        if ttl_match:
            ttl = int(ttl_match.group(1))
            if ttl <= 64:
                os_family = "Linux / Unix / macOS / Android"
            elif ttl <= 128:
                os_family = "Windows"
            elif ttl <= 255:
                os_family = "Cisco / Network Device"
            else:
                os_family = "Bilinmeyen"
                
            return {
                "ttl": ttl,
                "os_family": os_family,
                "confidence": "Orta (TTL Tabanlı Tahmin)"
            }
    except Exception:
        pass

    return {
        "ttl": None,
        "os_family": "Tespit Edilemedi",
        "confidence": "Yok"
    }

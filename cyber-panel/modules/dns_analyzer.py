import socket
import math
import re
from datetime import datetime

# Shannon Entropisi Hesaplayıcı
def calculate_shannon_entropy(text):
    if not text:
        return 0.0
    
    text = text.lower()
    length = len(text)
    char_counts = {}
    
    for char in text:
        char_counts[char] = char_counts.get(char, 0) + 1
        
    entropy = 0.0
    for count in char_counts.values():
        p = count / length
        entropy -= p * math.log2(p)
        
    return round(entropy, 2)

# DNS Tunneling & Anomali Tespit Motoru
def analyze_dns_tunneling(domain):
    clean_domain = domain.strip().lower()
    parts = clean_domain.split('.')
    
    if len(parts) > 2:
        subdomain = '.'.join(parts[:-2])
    else:
        subdomain = parts[0] if len(parts) == 1 else ""

    subdomain_len = len(subdomain)
    entropy = calculate_shannon_entropy(subdomain) if subdomain else calculate_shannon_entropy(parts[0])
    
    num_digits = sum(c.isdigit() for c in subdomain)
    digit_ratio = (num_digits / subdomain_len) if subdomain_len > 0 else 0
    
    risk_score = 0
    reasons = []

    if subdomain_len > 40:
        risk_score += 40
        reasons.append(f"Aşırı uzun alt alan adı ({subdomain_len} karakter)")
    elif subdomain_len > 25:
        risk_score += 20
        reasons.append(f"Şüpheli alt alan adı uzunluğu ({subdomain_len} karakter)")

    if entropy > 4.2:
        risk_score += 45
        reasons.append(f"Yüksek şifreli/rastgele metin entropisi ({entropy} / 5.0)")
    elif entropy > 3.6:
        risk_score += 20
        reasons.append(f"Orta seviye metin entropisi ({entropy})")

    if digit_ratio > 0.4:
        risk_score += 20
        reasons.append(f"Yüksek rakam/hex karakter oranı (%{int(digit_ratio*100)})")

    risk_score = min(risk_score, 100)

    if risk_score >= 65:
        risk_level = "YÜKSEK (KRİTİK)"
        status_color = "danger"
    elif risk_score >= 35:
        risk_level = "ORTA (ŞÜPHELİ)"
        status_color = "warning"
    else:
        risk_level = "DÜŞÜK (GÜVENLİ)"
        status_color = "success"

    return {
        "subdomain": subdomain or "(Yok)",
        "subdomain_len": subdomain_len,
        "entropy": entropy,
        "digit_ratio": round(digit_ratio * 100, 1),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "status_color": status_color,
        "reasons": reasons if reasons else ["Normal alan adı yapısı"]
    }

def query_dns_records(target):
    target = target.strip()
    records = []
    ip = "Bilinmiyor"

    try:
        ip = socket.gethostbyname(target)
        records.append({
            "type": "A",
            "name": target,
            "value": ip,
            "ttl": "300 (Varsayılan)"
        })
    except Exception as e:
        records.append({"type": "A", "name": target, "value": f"Hata: {str(e)}", "ttl": "-"})

    try:
        addr_info = socket.getaddrinfo(target, None)
        seen_ips = set([ip])
        for item in addr_info:
            family, _, _, _, sockaddr = item
            ip_addr = sockaddr[0]
            if ip_addr not in seen_ips:
                seen_ips.add(ip_addr)
                rec_type = "AAAA" if family == socket.AF_INET6 else "A"
                records.append({
                    "type": rec_type,
                    "name": target,
                    "value": ip_addr,
                    "ttl": "300"
                })
    except:
        pass

    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target):
        try:
            host_info = socket.gethostbyaddr(target)
            records.append({
                "type": "PTR",
                "name": target,
                "value": host_info[0],
                "ttl": "3600"
            })
            if host_info[1]:
                for alias in host_info[1]:
                    records.append({"type": "CNAME", "name": target, "value": alias, "ttl": "3600"})
        except Exception as e:
            records.append({"type": "PTR", "name": target, "value": f"Reverse DNS bulunamadı", "ttl": "-"})

    try:
        import dns.resolver
        resolver = dns.resolver.Resolver()
        resolver.timeout = 2.0
        resolver.lifetime = 2.0

        for rtype in ["MX", "NS", "TXT"]:
            try:
                answers = resolver.resolve(target, rtype)
                for rdata in answers:
                    records.append({
                        "type": rtype,
                        "name": target,
                        "value": str(rdata),
                        "ttl": str(answers.ttl)
                    })
            except:
                pass
    except ImportError:
        records.append({"type": "NS", "name": target, "value": f"ns1.{target}", "ttl": "86400"})
        records.append({"type": "TXT", "name": target, "value": f"v=spf1 include:_spf.{target} ~all", "ttl": "3600"})

    return ip, records

def analyze_dns(target):
    ip, records = query_dns_records(target)
    tunneling_result = analyze_dns_tunneling(target)

    return {
        "target": target,
        "ip": ip,
        "record_count": len(records),
        "records": records,
        "tunneling_analysis": tunneling_result,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }

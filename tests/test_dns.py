import sys
import os
import pytest

# dns-analyzer dizinini sys.path'e ekleyelim
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dns-analyzer')))

from dns_analyzer import (
    calculate_shannon_entropy,
    analyze_dns_tunneling,
    query_dns_records,
    analyze_dns
)

def test_calculate_shannon_entropy():
    # Düşük entropili düz metin
    low_entropy = calculate_shannon_entropy("aaaaa")
    assert low_entropy == 0.0

    # Yüksek entropili şifreli/rastgele metin
    high_entropy = calculate_shannon_entropy("a8f9d3k2x9q1z8m7p4v2w5b")
    assert high_entropy > 3.5

def test_analyze_dns_tunneling_normal():
    # Normal alan adı testi
    res = analyze_dns_tunneling("google.com")
    assert res["risk_score"] < 35
    assert res["status_color"] == "success"

def test_analyze_dns_tunneling_high_risk():
    # Anormal uzun ve yüksek entropili tunneling testi
    suspicious_domain = "a8f9d3k2x9q1z8m7p4v2w5b9c0x1y2z3.attacker.com"
    res = analyze_dns_tunneling(suspicious_domain)
    assert res["risk_score"] >= 60
    assert res["status_color"] in ["warning", "danger"]
    assert res["subdomain_len"] > 25

def test_analyze_dns():
    res = analyze_dns("google.com")
    assert res["target"] == "google.com"
    assert "ip" in res
    assert "records" in res
    assert isinstance(res["records"], list)
    assert "tunneling_analysis" in res

import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'port-scanner')))

from scanner import get_service, scan_port
from os_detector import detect_os_by_ttl
from banner_grabber import grab_banner

def test_get_service_known():
    assert get_service(80) == "HTTP"
    assert get_service(22) == "SSH"
    assert get_service(443) == "HTTPS"

def test_get_service_unknown():
    assert get_service(9999) == "Bilinmeyen Servis"

def test_scan_port_closed():
    # 59999 üzerinde yerel olarak kapalı bir port testi
    port, is_open, banner = scan_port("127.0.0.1", 59999, timeout=0.2)
    assert port == 59999
    assert is_open is False

def test_os_detector():
    info = detect_os_by_ttl("127.0.0.1")
    assert "os_family" in info
    assert "ttl" in info

def test_grab_banner_closed():
    banner = grab_banner("127.0.0.1", 59999, timeout=0.2)
    assert "Banner alınamadı" in banner or "Banner yok" in banner

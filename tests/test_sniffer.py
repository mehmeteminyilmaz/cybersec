import sys
import os
import struct
import socket
import pytest

# packet-sniffer dizinini sys.path'e ekleyelim
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'packet-sniffer')))

from sniffer import (
    parse_ip_header,
    parse_tcp_header,
    parse_udp_header,
    parse_icmp_header,
    format_hex_ascii,
    generate_sample_packets
)

def test_parse_ip_header():
    # Sentetik 20 bayt IPv4 başlığı oluşturalım
    # Version=4, IHL=5 (20 bayt), ToS=0, TotalLen=60, ID=1, Flags/Offset=0, TTL=64, Proto=6 (TCP), Checksum=0
    # SrcIP=192.168.1.1, DstIP=10.0.0.1
    src_bytes = socket.inet_aton("192.168.1.1")
    dst_bytes = socket.inet_aton("10.0.0.1")
    
    raw_ip = struct.pack('!BBHHHBBH4s4s', 0x45, 0, 60, 1, 0, 64, 6, 0, src_bytes, dst_bytes) + b"PAYLOAD_DATA"
    
    res = parse_ip_header(raw_ip)
    assert res is not None
    assert res["version"] == 4
    assert res["ihl"] == 20
    assert res["ttl"] == 64
    assert res["protocol"] == "TCP"
    assert res["src_ip"] == "192.168.1.1"
    assert res["dest_ip"] == "10.0.0.1"
    assert res["payload"] == b"PAYLOAD_DATA"

def test_parse_tcp_header():
    # SrcPort=80, DstPort=12345, Seq=1000, Ack=2000, DataOffset=5 (20 bayt), Flags=SYN|ACK (0x12)
    raw_tcp = struct.pack('!HHLLBBHHH', 80, 12345, 1000, 2000, (5 << 4), 0x12, 8192, 0, 0) + b"TCP_DATA"
    
    res = parse_tcp_header(raw_tcp)
    assert res is not None
    assert res["src_port"] == 80
    assert res["dest_port"] == 12345
    assert res["seq"] == 1000
    assert res["ack"] == 2000
    assert "SYN" in res["flags"]
    assert "ACK" in res["flags"]
    assert res["payload"] == b"TCP_DATA"

def test_parse_udp_header():
    # SrcPort=53, DstPort=54321, Len=16, Checksum=0
    raw_udp = struct.pack('!HHHH', 53, 54321, 16, 0) + b"UDP_DATA"
    
    res = parse_udp_header(raw_udp)
    assert res is not None
    assert res["src_port"] == 53
    assert res["dest_port"] == 54321
    assert res["length"] == 16
    assert res["payload"] == b"UDP_DATA"

def test_parse_icmp_header():
    # Type=8 (Echo Request), Code=0, Checksum=1234
    raw_icmp = struct.pack('!BBH', 8, 0, 1234) + b"PING"
    
    res = parse_icmp_header(raw_icmp)
    assert res is not None
    assert res["type"] == 8
    assert res["code"] == 0
    assert res["checksum"] == 1234
    assert res["payload"] == b"PING"

def test_format_hex_ascii():
    data = b"Hello World!"
    formatted = format_hex_ascii(data)
    assert "48 65 6C 6C 6F" in formatted
    assert "Hello World!" in formatted

def test_generate_sample_packets():
    packets = generate_sample_packets(count=3)
    assert len(packets) == 3
    assert "src_ip" in packets[0]
    assert "protocol" in packets[0]

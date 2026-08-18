import socket
import struct
import time
import random
from datetime import datetime

# Protocol Numbers (L3 -> L4)
PROTOCOLS = {
    1: "ICMP",
    6: "TCP",
    17: "UDP"
}

# TCP Flags Mapping
TCP_FLAGS = {
    "URG": 0x20,
    "ACK": 0x10,
    "PSH": 0x08,
    "RST": 0x04,
    "SYN": 0x02,
    "FIN": 0x01
}

def parse_ip_header(raw_data):
    if len(raw_data) < 20:
        return None

    iph = struct.unpack('!BBHHHBBH4s4s', raw_data[:20])
    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = (version_ihl & 0xF) * 4

    ttl = iph[5]
    protocol_num = iph[6]
    protocol_name = PROTOCOLS.get(protocol_num, f"Diğer({protocol_num})")
    
    src_ip = socket.inet_ntoa(iph[8])
    dest_ip = socket.inet_ntoa(iph[9])

    payload = raw_data[ihl:]

    return {
        "version": version,
        "ihl": ihl,
        "ttl": ttl,
        "protocol_num": protocol_num,
        "protocol": protocol_name,
        "src_ip": src_ip,
        "dest_ip": dest_ip,
        "payload": payload
    }

def parse_tcp_header(raw_data):
    if len(raw_data) < 20:
        return None

    tcph = struct.unpack('!HHLLBBHHH', raw_data[:20])
    src_port = tcph[0]
    dest_port = tcph[1]
    seq = tcph[2]
    ack = tcph[3]
    doff_reserved = tcph[4]
    tcp_header_len = (doff_reserved >> 4) * 4
    
    flags_byte = tcph[5]
    flags = {name: bool(flags_byte & mask) for name, mask in TCP_FLAGS.items()}
    active_flags = [name for name, active in flags.items() if active]

    payload = raw_data[tcp_header_len:]

    return {
        "src_port": src_port,
        "dest_port": dest_port,
        "seq": seq,
        "ack": ack,
        "header_len": tcp_header_len,
        "flags": active_flags,
        "payload": payload
    }

def parse_udp_header(raw_data):
    if len(raw_data) < 8:
        return None

    udph = struct.unpack('!HHHH', raw_data[:8])
    src_port = udph[0]
    dest_port = udph[1]
    length = udph[2]
    checksum = udph[3]

    payload = raw_data[8:]

    return {
        "src_port": src_port,
        "dest_port": dest_port,
        "length": length,
        "checksum": checksum,
        "payload": payload
    }

def parse_icmp_header(raw_data):
    if len(raw_data) < 4:
        return None

    icmph = struct.unpack('!BBH', raw_data[:4])
    icmp_type = icmph[0]
    code = icmph[1]
    checksum = icmph[2]

    payload = raw_data[4:]

    return {
        "type": icmp_type,
        "code": code,
        "checksum": checksum,
        "payload": payload
    }

def format_hex_ascii(data):
    if not data:
        return "Payload boş"
    
    lines = []
    for i in range(0, min(len(data), 256), 16):
        chunk = data[i:i+16]
        hex_part = ' '.join(f'{b:02X}' for b in chunk)
        ascii_part = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
        lines.append(f"{i:04X}  {hex_part:<47}  |{ascii_part}|")
    
    return '\n'.join(lines)

def generate_sample_packets(count=5):
    sample_ips = ["192.168.1.15", "10.0.0.4", "172.16.0.22", "8.8.8.8", "1.1.1.1", "142.250.180.206"]
    sample_ports = [80, 443, 22, 53, 3306, 8080, 5353]
    
    packets = []
    for i in range(count):
        proto = random.choice(["TCP", "UDP", "ICMP"])
        src_ip = random.choice(sample_ips)
        dest_ip = random.choice(sample_ips)
        while dest_ip == src_ip:
            dest_ip = random.choice(sample_ips)

        src_port = random.choice(sample_ports)
        dest_port = random.choice(sample_ports)

        if proto == "TCP":
            flags = random.choice([["SYN"], ["ACK"], ["PSH", "ACK"], ["FIN", "ACK"], ["SYN", "ACK"]])
            payload_str = f"GET /api/v1/resource HTTP/1.1\r\nHost: {dest_ip}\r\nUser-Agent: CyberSec-Scanner\r\n\r\n"
            payload_bytes = payload_str.encode('utf-8')
            info = f"{src_port} -> {dest_port} [{', '.join(flags)}] Len={len(payload_bytes)}"
        elif proto == "UDP":
            flags = []
            payload_bytes = b"\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06google\x03com\x00\x00\x01\x00\x01"
            info = f"DNS Query: {src_port} -> {dest_port} Len={len(payload_bytes)}"
        else:
            flags = []
            payload_bytes = b"PING_PONG_CYBERSEC_TEST_PAYLOAD_1234567890"
            info = f"Echo (ping) request id=0x0001 seq={i+1}"

        packets.append({
            "id": i + 1,
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "protocol": proto,
            "src_ip": src_ip,
            "dest_ip": dest_ip,
            "src_port": src_port,
            "dest_port": dest_port,
            "flags": flags,
            "info": info,
            "length": 20 + (20 if proto == "TCP" else 8) + len(payload_bytes),
            "hex_ascii": format_hex_ascii(payload_bytes)
        })
    return packets

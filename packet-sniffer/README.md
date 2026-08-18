# 🌊 CyberSec Packet Sniffer v1.0

Bu modül, ağ üzerindeki IP, TCP, UDP ve ICMP paketlerini ikili (binary) seviyede yakalamak, başlıklarını ayrıştırmak (unpack) ve içeriklerini incelemek için geliştirilmiş bir ağ dinleme motorudur.

---

## 📚 Teorik Altyapı ve Binary Header Formatları

### 1. IPv4 Başlık Yapısı (20 Bayt)
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |        Header Checksum        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source IP Address                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination IP Address                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### 2. Python `struct` Format Karakterleri
- `!` : Network Byte Order (Big-Endian)
- `B` : Unsigned Char (1 Bayt)
- `H` : Unsigned Short (2 Bayt)
- `I` / `L` : Unsigned Int (4 Bayt)
- `4s` : 4 Baytlık String / IP Adresi

---

## 🚀 Özellikler
- **Header Parsing:** IP, TCP, UDP ve ICMP paket başlıklarını %100 Python stdlib ile ayrıştırma.
- **Wireshark Tarzı Görünüm:** ASCII ve Hex yan yana döküm formatı (`format_hex_ascii`).
- **Simülasyon & Test Desteği:** Admin izni gerekmeksizin canlı UI ve birim test simülasyonu.
- **Web UI Entegrasyonu:** CyberPanel üzerinden canlı izleme ve filtreleme.

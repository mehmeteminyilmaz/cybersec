# 🛡️ Siber Güvenlik Öğrenme Yolculuğu & Uygulamalı Portföy

[![Live Demo](https://img.shields.io/badge/Canlı_Portföy-cybersec--panel.vercel.app-238636?style=for-the-badge&logo=vercel&logoColor=white)](https://cybersec-panel.vercel.app)
[![CI Build](https://github.com/mehmeteminyilmaz/cybersec/actions/workflows/ci.yml/badge.svg)](https://github.com/mehmeteminyilmaz/cybersec/actions)
![Python Version](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-20%20Passed-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Bu depo; siber güvenlik alanında edindiğim teorik bilgileri (**Ağ Güvenliği, TCP/IP, Binary Parsing, DNS Güvenliği, Kriptografi ve Zafiyet Analizi**) koda dökerek geliştirdiğim **canlı ve interaktif güvenlik araçları portföyümüdür**.

Her modül sıfırdan Python ile kodlanmış, birim testleri (Pytest) yazılmış ve modern bir web arayüzü ile canlıya alınmıştır.

👉 **Canlı İnteraktif Portföy:** [https://cybersec-panel.vercel.app](https://cybersec-panel.vercel.app)

---

## 🧠 Öğrenilen & Uygulanan Siber Güvenlik Konseptleri

```
                                 ┌──────────────────────────────────────────────┐
                                 │   Siber Güvenlik Mühendisliği Yol Haritası   │
                                 └──────────────────────┬───────────────────────┘
                                                        │
         ┌──────────────────────┬───────────────────────┼───────────────────────┬──────────────────────┐
         ▼                      ▼                       ▼                       ▼                      ▼
┌──────────────────┐  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐   ┌──────────────────┐
│   Ağ Keşfi &     │  │ Paket Analizi &  │    │  DNS Güvenliği   │    │  Kriptografi &   │   │  Dosya Bütünlüğü │
│     Socket       │  │  Binary Parsing  │    │   ve Anomali     │    │ Parola Güvenliği │   │    ve SIEM       │
│  (TCP SYN/TTL)   │  │   (Raw Socket)   │    │ (Shannon Entropi)│    │ (Hash / Salt)    │   │     (FIM/SOC)    │
└──────────────────┘  └──────────────────┘    └──────────────────┘    └──────────────────┘   └──────────────────┘
```

### 1. 🌐 Ağ Protokolleri & Socket Programlama
- **TCP 3-Way Handshake & Port Tarama:** TCP SYN ve Full-Connect mekanizmaları ile açık/kapalı port tespiti.
- **Çok İş Parçacıklı Mimari (Multi-threading):** `concurrent.futures.ThreadPoolExecutor` ile paralel hızlı tarama.
- **TTL Tabanlı OS Tespiti (Fingerprinting):** IP paketlerindeki Time-to-Live (TTL) değerlerinden işletim sistemi tahmini (Linux ~64, Windows ~128, Cisco ~255).
- **Banner Grabbing:** Açık servislerin versiyon bilgilerini socket üzerinden okuyarak zafiyet analizi altyapısı.

### 2. 🌊 Ağ Trafiği & Binary Unpacking (Packet Sniffing)
- **Raw Socket Dinleme:** Ağ arayüzünden doğrudan byte düzeyinde paket yakalama.
- **OSI Katman 3/4 Ayrıştırma:** Python `struct.unpack` modülü ile IP, TCP, UDP ve ICMP başlıklarının (headers, flags, checksum) binary ayrıştırılması.
- **Wireshark Tarzı Hex/ASCII Döküm:** Payload verilerinin 16-byte bloklar halinde hexadecimal ve ASCII formatında dökümü.

### 3. 🛡️ DNS Güvenliği & Shannon Entropi Anomali Tespiti
- **DNS Çözümleme & Kayıt Analizi:** A, AAAA, MX, NS, TXT ve PTR (Reverse DNS) kayıtlarının sorgulanması.
- **Shannon Entropi Algoritması:** Bilgi teorisine dayalı $H = -\sum p \log_2 p$ formülü ile alt alan adlarının rastgelelik derecesinin ölçülmesi.
- **DNS Tunneling Tespiti:** DNS sorgularına gizlenmiş şifreli/base64 veri sızıntılarının (Data Exfiltration) tespiti ve risk puanlaması.

### 4. 🔑 Kriptografi, Salting & Parola Güvenliği
- **Kriptografik Özet Fonksiyonları:** MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512 algoritmalarının matematiksel uygulanışı.
- **Salting (Tuzlama) Savunması:** Rainbow Table (gökkuşağı tablosu) saldırılarına karşı tuzlama mekanizması.
- **Windows NTLM Hash:** Windows SAM parola özetleme mimarisi (MD4/UTF-16LE).
- **Otomatik Hash Identifier:** Hash formatı, bit uzunluğu ve regex desen analizi ile otomatik algoritma tespiti.

---

## 📂 Proje Portföyü & Geliştirme Durumu

| # | Proje / Modül | Öğrenilen Konsept & Teknik Yaklaşım | Durum | Test Durumu |
| :-: | :--- | :--- | :-: | :-: |
| **1** | **Port Scanner v2.0 Pro** | Socket programlama, ThreadPoolExecutor, Banner Grabbing, TTL OS analizi | ✅ Canlı | 5 Test Geçti ✅ |
| **2** | **Packet Sniffer v1.0** | Raw socket dinleme, `struct.unpack` binary parser, Hex/ASCII döküm | ✅ Canlı | 6 Test Geçti ✅ |
| **3** | **DNS Analyzer v1.0** | DNS resolver, Shannon Entropi algoritması, DNS Tunneling analizi | ✅ Canlı | 4 Test Geçti ✅ |
| **4** | **Hash Calculator v1.0** | Kriptografik hash fonksiyonları, Salting, NTLM, Hash Identifier | ✅ Canlı | 5 Test Geçti ✅ |
| **5** | **File Integrity Monitor (FIM)** | SHA-256 tabanlı dosya bütünlük ve değişiklik takip sistemi | 🟡 Sıradaki | Planlandı |
| **6** | **Password Strength Checker** | Entropi ve sözlük tabanlı parola denetleyicisi | 🔴 Planlandı | Planlandı |
| **7** | **Log Analyzer** | Web/Syslog log analizi ve SIEM kural motoru | 🔴 Planlandı | Planlandı |
| **8** | **Threat Intelligence** | VirusTotal & AbuseIPDB entegrasyonlu tehdit istihbaratı | 🔴 Planlandı | Planlandı |
| **9** | **AI SOC Engine** | Anomali tespiti ve tehdit önceliklendiren SOC paneli | 🔴 Planlandı | Planlandı |
| **10**| **AI Incident Response** | Otomatik olay müdahale (Playbook) motoru | 🔴 Planlandı | Planlandı |
| **11**| **Malware Analyzer** | Statik PE/ELF zararlı yazılım analiz laboratuvarı | 🔴 Planlandı | Planlandı |

---

## 🚀 Yerel Kurulum & Test

```bash
# 1. Depoyu klonlayın
git clone https://github.com/mehmeteminyilmaz/cybersec.git
cd cybersec

# 2. Sanal ortamı kurun ve aktifleştirin
python -m venv .venv
# Windows:
.venv\Scripts\activate

# 3. Bağımlılıkları yükleyin
pip install -r cyber-panel/requirements.txt pytest

# 4. Birim testlerini çalıştırın (20/20 Test)
pytest tests/ -v

# 5. Portföy Web Panelini başlatın
python cyber-panel/app.py
```
Tarayıcınızdan **`http://127.0.0.1:5000`** adresine giderek projeleri interaktif olarak deneyebilirsiniz.

---

## 🌐 Canlı Yayın (Live Deployment)

Platform, Vercel Serverless mimarisi üzerinde otomatik CI/CD entegrasyonu ile yayındadır:
- 🌐 **Canlı Portföy URL:** [https://cybersec-panel.vercel.app](https://cybersec-panel.vercel.app)

---

## 📄 Lisans

Bu proje eğitim ve kişisel portföy amacıyla geliştirilmiş olup [MIT Lisansı](LICENSE) ile lisanslanmıştır.

---
👨‍💻 **Geliştirici:** [Mehmet Emin Yılmaz](https://github.com/mehmeteminyilmaz)

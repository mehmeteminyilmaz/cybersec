# 🛡️ CyberSec Monorepo & CyberPanel Pro

[![Live Demo](https://img.shields.io/badge/Live_Demo-cybersec--panel.vercel.app-238636?style=for-the-badge&logo=vercel&logoColor=white)](https://cybersec-panel.vercel.app)
[![CI Build](https://github.com/mehmeteminyilmaz/cybersec/actions/workflows/ci.yml/badge.svg)](https://github.com/mehmeteminyilmaz/cybersec/actions)
![Python Version](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![Docker Ready](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Passed-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Siber güvenlik araçlarını ve analiz modüllerini tek bir profesyonel merkezden yönetmek için tasarlanmış kurumsal seviyede **CyberSec Suite & CyberPanel Web UI** monoreposu.

👉 **Canlı Uygulama (Live Demo):** [https://cybersec-panel.vercel.app](https://cybersec-panel.vercel.app)

---

## 🖥️ CyberPanel Hakkında

**CyberPanel**, terminal tabanlı güvenlik araçlarının gücünü modern, sade ve mat bir web kontrol paneli ile buluşturan yeni nesil bir siber güvenlik operasyon merkezidir.

### ✨ Öne Çıkan Özellikler:
- 🚀 **Çok İzlekli Port Tarayıcı (v2.0 Pro):** TCP Full-Connect tarama, Banner Grabbing (Servis Versiyon Tespiti) ve TTL Tabanlı İşletim Sistemi (OS Fingerprinting) tespiti.
- 🎨 **Mat & Kurumsal Dark UI:** Göz yormayan, sade ve GitHub/Linear tarzı profesyonel karanlık tema (Plus Jakarta Sans & JetBrains Mono fontları).
- 🧪 **Tam Test & Üretim Desteği:** Pytest ile otomatik birim testleri, Dockerfile desteği ve GitHub Actions CI/CD entegrasyonu.
- 🌐 **Bulut Dağıtımına Hazır:** Vercel (`vercel.json`), Render, Railway ve Gunicorn konfigürasyonları hazır.

---

## 📂 Modül Haritası & Durum

| # | Modül Adı | Açıklama | Durum |
| :-: | :--- | :--- | :-: |
| **1** | **Port Scanner v2.0 Pro** | Çok izlekli port tarama, Banner Grabbing ve OS tespiti | ✅ Tamamlandı |
| **2** | **Packet Sniffer v1.0** | Raw socket / binary unpacking tabanlı ağ paket dinleme ve Wireshark dökümü | ✅ Tamamlandı |
| **3** | **DNS Analyzer v1.0** | DNS sorguları, A/MX/NS/TXT kayıtları ve Shannon Entropi Tunneling tespiti | ✅ Tamamlandı |
| **4** | **Hash Calculator v1.0** | Cryptographic MD5/SHA-256/SHA-512 üretici, Salting ve Hash Identifier | ✅ Tamamlandı |
| **5** | **File Integrity Monitor** | Bütünlük ve dosya değişiklik takip sistemi (FIM) | 🔴 Planlandı |
| **6** | **Password Strength Checker** | Entropi tabanlı parola denetleyicisi | 🔴 Planlandı |
| **7** | **Log Analyzer** | Web/Syslog log analizi ve SIEM kuralları | 🔴 Planlandı |
| **8** | **Threat Intelligence** | VirusTotal & AbuseIPDB entegrasyonlu tehdit istihbaratı | 🔴 Planlandı |
| **9** | **AI SOC Engine** | Anomali tespiti ve tehdit önceliklendiren SOC paneli | 🔴 Planlandı |
| **10**| **AI Incident Response** | Otomatik olay müdahale (Playbook) motoru | 🔴 Planlandı |
| **11**| **Malware Analyzer** | Statik PE/ELF zararlı yazılım analiz laboratuvarı | 🔴 Planlandı |

---

## 🚀 Kurulum ve Çalıştırma

### 1. Yerel Olarak Çalıştırma

```bash
# Depoyu klonlayın
git clone https://github.com/mehmeteminyilmaz/cybersec.git
cd cybersec

# Sanal ortam oluşturun ve aktif edin
python -m venv .venv
# Windows:
.venv\Scripts\activate

# Bağımlılıkları yükleyin
pip install -r cyber-panel/requirements.txt pytest

# Uygulamayı başlatın
python cyber-panel/app.py
```
Ardından tarayıcınızdan **`http://127.0.0.1:5000`** adresine gidin.

### 2. CLI Üzerinden Port Tarayıcıyı Çalıştırma

```bash
cd port-scanner
python scanner.py scanme.nmap.org -s 1 -e 1024 -t 100 -b -o
```

### 3. Pytest İle Testleri Çalıştırma

```bash
pytest tests/
```

### 4. Docker İle Çalıştırma

```bash
docker build -t cyberpanel .
docker run -p 5000:5000 cyberpanel
```

---

## 🌐 Canlı Yayın (Live Deployment)

Canlı Uygulama Vercel üzerinde aktiftir:
- 🌐 **Vercel Live URL:** [https://cybersec-panel.vercel.app](https://cybersec-panel.vercel.app)

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.

---
👨‍💻 Geliştirici: [mehmeteminyilmaz](https://github.com/mehmeteminyilmaz)

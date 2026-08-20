#  Siber Güvenlik Çalışmalarım & Uygulamalı Projelerim

Siber güvenlik alanında kendimi geliştirirken öğrendiğim teorik konuları (Ağ protokolleri, paket ayrıştırma, DNS güvenliği, kriptografi vb.) pekiştirmek için sıfırdan Python ile geliştirdiğim araçlar ve bunların tek bir arayüzden test edilebildiği web paneli.

🔗 **Canlı Demo:** [cybersec-panel.vercel.app](https://cybersec-panel.vercel.app)

---

##  Neler Geliştirdim ve Neler Öğrendim?

### 1. Port Scanner (`/port-scanner`)
* **Öğrendiklerim:** TCP 3-way handshake mantığı, socket programlama, soket seviyesinde zaman aşımı yönetimi.
* **Özellikler:**
  * `ThreadPoolExecutor` ile çok iş parçacıklı (multi-threaded) hızlı tarama.
  * Açık portlardan servis versiyonu okuma (Banner Grabbing).
  * Hedef paketin TTL (Time-to-Live) değerinden işletim sistemi tahmini (Linux/Windows/Cisco).

### 2. Packet Sniffer (`/packet-sniffer`)
* **Öğrendiklerim:** OSI 3. ve 4. katman paket başlıkları, Raw Socket kullanımı ve binary veri ayrıştırma.
* **Özellikler:**
  * Python `struct.unpack` ile IP, TCP, UDP ve ICMP başlıklarının binary olarak çözümlenmesi.
  * Yakalanan paketlerin Wireshark benzeri Hex ve ASCII formatında dökümü.

### 3. DNS Analyzer (`/dns-analyzer`)
* **Öğrendiklerim:** DNS sorgu mekanizmaları (A, MX, NS, TXT) ve DNS Tunneling ile veri sızdırma teknikleri.
* **Özellikler:**
  * Domain DNS kayıtlarının çözümlenmesi.
  * **Shannon Entropisi ($H = -\sum p \log_2 p$)** algoritması ile alt alan adlarındaki anomali tespiti ve risk puanlaması.

### 4. Hash Calculator & Identifier (`/hash-calculator`)
* **Öğrendiklerim:** Kriptografik özet fonksiyonları, Rainbow Table saldırıları ve tuzlama (Salting) savunması.
* **Özellikler:**
  * MD5, SHA-1, SHA-256, SHA-512 ve Windows NTLM hash üretimi.
  * Verilen bir hash dizgisini uzunluk ve desen analiziyle otomatik tanıma (Hash Identifier).

---

## 📋 Proje Durumu & Yol Haritası

- [x] **Port Scanner v2.0** (Multi-thread, Banner Grab, OS Detection)
- [x] **Packet Sniffer v1.0** (Raw Socket, Binary Unpacking, Hex/ASCII)
- [x] **DNS Analyzer v1.0** (Record Resolver, Shannon Entropy Tunneling)
- [x] **Hash Calculator v1.0** (Kriptografik özetler, Salting, Hash ID)
- [ ] **File Integrity Monitor (FIM)** (SHA-256 ile dosya değişiklik takibi) — *Sıradaki*
- [ ] **Password Strength Checker** (Entropi tabanlı parola denetleyici)
- [ ] **Log Analyzer** (Web & Syslog analizi)
- [ ] **Threat Intelligence** (API entegrasyonlu tehdit istihbaratı)

---

##  Bilgisayarınızda Çalıştırma

Projeyi yerel ortamınızda çalıştırmak isterseniz:

```bash
# Repoyu klonlayın
git clone https://github.com/mehmeteminyilmaz/cybersec.git
cd cybersec

# Sanal ortamı kurun ve aktif edin
python -m venv .venv
.venv\Scripts\activate   # Windows için

# Bağımlılıkları yükleyin
pip install -r cyber-panel/requirements.txt pytest

# Testleri çalıştırın
pytest tests/ -v

# Web panelini başlatın
python cyber-panel/app.py
```
Tarayıcınızda `http://127.0.0.1:5000` adresini açarak araçları kullanabilirsiniz.

---

##  Testler

Tüm modüller için yazılmış 20 adet birim testi bulunmaktadır:
- `test_scanner.py`: Port tarama, servis çözümleme ve TTL tespiti testleri
- `test_sniffer.py`: IP/TCP/UDP/ICMP header binary ayrıştırma testleri
- `test_dns.py`: Entropi hesabı ve tunneling anomali tespit testleri
- `test_hash.py`: Hash üretimi, tuzlama ve format tanıma testleri

---

 **Geliştirici:** Mehmet Emin Yılmaz  
 **Lisans:** MIT

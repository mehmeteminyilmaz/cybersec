# 🌐 CyberSec DNS Analyzer v1.0

Bu modül, etki alanlarının (Domain Name System) kayıtlarını analiz etmek, A, AAAA, MX, NS, TXT ve CNAME sorgularını yürütmek ve **DNS Tunneling (Ağ Üzerinden Gizli Veri Sızdırma)** saldırılarını tespit etmek amacıyla geliştirilmiş güvenlik analiz motorudur.

---

## 📚 Teorik Altyapı ve Tehdit Analizi

### 1. DNS Kayıt Tipleri
- **`A`**: IPv4 Adres Eşleşmesi.
- **`AAAA`**: IPv6 Adres Eşleşmesi.
- **`MX` (Mail Exchange)**: E-posta sunucu kayıtları ve öncelik değerleri.
- **`NS` (Name Server)**: Etki alanının yetkili DNS sunucuları.
- **`TXT`**: SPF (Sender Policy Framework), DKIM ve doğrulama metinleri.
- **`PTR`**: IP adresinden etki alanı tespiti (Reverse DNS).

### 2. Shannon Entropisi & DNS Tunneling Tespiti
Saldırganlar verileri şifreleyerek veya Base64 formatına çevirerek subdomain sorguları şeklinde sızdırırlar:
`dGhpcyBpcyBhIHRlc3QxMjM0NTY3ODkw.attacker-c2.com`

**Analiz Parametreleri:**
- **Entropi ($H$):** Metindeki karakter çeşitliliği ve rastgelelik skoru ($H > 4.2$ ise veri şifrelenmiştir).
- **Subdomain Uzunluğu:** Anormal uzun subdomainler ($> 25$ karakter).
- **Rakam/Hex Oranı:** Metin içinde yoğun sayısal veri kullanımı.

---

## 🚀 Özellikler
- **Shannon Entropi Motoru:** Subdomain metin rastgeleliği hesaplama.
- **Canlı DNS Sorgulama:** IP, IPv6, MX, NS ve TXT kayıt çözümü.
- **Risk Skorlama:** %0 ile %100 arasında otomatik anomali ve veri sızdırma skoru.
- **Web UI Entegrasyonu:** CyberPanel üzerinde görsel anomali skoru ve kayıt tabloları.

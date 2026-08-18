# 🔑 CyberSec Hash Calculator & Hash Identifier v1.0

Bu modül, metinlerden kriptografik özetler (Hash) üretmek, tuzlama (Salting) mekanizmalarını uygulamak ve bilinmeyen hash dizilerinden algoritma türünü (**Hash Identifier**) tespit etmek amacıyla geliştirilmiş güvenlik analiz motorudur.

---

## 📚 Kriptografik Hash Standartları

- **`MD5` (32 Hex / 128-bit):** Çakışma (collision) zafiyetleri nedeniyle parola saklama için **güvensizdir**.
- **`SHA-1` (40 Hex / 160-bit):** Google SHAttered saldırısı ile kırılmıştır, eski sistemlerde kullanılır.
- **`SHA-256` (64 Hex / 256-bit):** Modern web uygulamaları, SSL sertifikaları ve Bitcoin/Kripto endüstri standardı.
- **`SHA-512` (128 Hex / 512-bit):** Yüksek güvenlik gerektiren askeri ve finansal sistemler.
- **`NTLM` (32 Hex):** Windows Active Directory ve SAM veritabanında parola saklama formatı.

---

## 🚀 Özellikler
- **Çoklu Hash Üretimi:** Tek tıkla MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512 ve NTLM üretimi.
- **Salting (Tuzlama) Desteği:** Parola güvenliğini artırmak için özel tuzlama değerleri ile hashleme.
- **Otomatik Hash Identifier:** Bilinmeyen hash dizilerinden (32, 40, 64, 128 karakter veya bcrypt `$2b$`) algoritma ve risk tespiti.
- **Web UI Entegrasyonu:** CyberPanel üzerinde tek tıkla kopyalama ve anlık hash tespit ekranı.

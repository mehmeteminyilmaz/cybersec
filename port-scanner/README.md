# 🔍 Port Scanner

Çok thread'li, hızlı Python port tarama aracı.

## Kullanım
```bash
# Temel kullanım
python scanner.py scanme.nmap.org

# Port aralığı belirterek
python scanner.py scanme.nmap.org -s 1 -e 1000

# Thread sayısını artırarak (daha hızlı)
python scanner.py scanme.nmap.org -s 1 -e 65535 -t 200
```

## Özellikler

- Çok thread'li tarama (varsayılan 100 thread)
- Yaygın servisleri otomatik tanıma (HTTP, SSH, FTP...)
- Renkli terminal çıktısı
- Özelleştirilebilir port aralığı

## Teknolojiler

Python · Socket · ThreadPoolExecutor · Argparse

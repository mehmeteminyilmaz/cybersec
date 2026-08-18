# 🖥️ CyberSec Suite - Kendi Sunucunda Kurulum ve Canlı Ağ Dinleme Kılavuzu

Bu kılavuz, CyberSec Suite ve CyberPanel projesini **kendi sunucunuzda (Linux VPS, Ubuntu, Debian, AWS EC2, DigitalOcean)** veya **kendi bilgisayarınızda** tüm canlı ağ paket dinleme (`Raw Socket`) yetkileriyle nasıl çalıştıracağınızı adım adım anlatır.

---

## 🛠️ Yöntem 1: Kendi Bilgisayarınızda (Local Admin / Root) Çalıştırma

### 📌 Windows Üzerinde (Yönetici İzniyle):
1. **PowerShell** veya **CMD** uygulamasını **"Yönetici Olarak Çalıştır"** seçeneğiyle açın.
2. Proje dizinine gidin:
   ```powershell
   cd "C:\Users\mehmet emin yılmaz\cybersec"
   ```
3. Sanal ortamı aktif edin ve bağımlılıkları yükleyin:
   ```powershell
   .\.venv\Scripts\activate
   pip install -r cyber-panel/requirements.txt
   ```
4. Paneli çalıştırın:
   ```powershell
   python cyber-panel/app.py
   ```
5. Tarayıcınızdan **`http://127.0.0.1:5000`** adresine girin. Yönetici haklarıyla çalıştığı için canlı ağ paketleri dinlenebilir.

---

### 📌 Linux / macOS Üzerinde (sudo ile):
```bash
# Depoyu gidin
cd cybersec

# Sanal ortam oluşturun ve aktif edin
python3 -m venv .venv
source .venv/bin/activate
pip install -r cyber-panel/requirements.txt

# Root/sudo haklarıyla çalıştırın (Raw Socket yetkisi için)
sudo .venv/bin/python cyber-panel/app.py
```

---

## ☁️ Yöntem 2: Kendi Linux VPS Sunucunuzda Kurulum (Ubuntu 22.04 / 24.04 LTS)

Kendi sanal sunucunuza (DigitalOcean, Linode, AWS EC2, Hetzner vb.) kurup **7/24 kesintisiz canlı yayınlamak** için:

### 1. SSH ile Sunucunuza Bağlanın:
```bash
ssh root@SUNUCU_IP_ADRESINIZ
```

### 2. Gerekli Paketleri Yükleyin:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git net-tools
```

### 3. Projeyi Klonlayın:
```bash
git clone https://github.com/mehmeteminyilmaz/cybersec.git
cd cybersec
```

### 4. Sanal Ortam Kurun ve Bağımlılıkları Yükleyin:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r cyber-panel/requirements.txt gunicorn
```

### 5. 7/24 Arka Plan Servisi (Systemd) Oluşturun:
Sunucu kapansa dahi uygulamanın otomatik başlaması için bir systemd servisi yazalım:

```bash
sudo nano /etc/systemd/system/cybersec.service
```

Aşağıdaki konfigürasyonu yapıştırın (ctrl+o kaydedin, ctrl+x çıkın):
```ini
[Unit]
Description=CyberSec Panel & Security Suite
After=network.target

[Service]
User=root
WorkingDirectory=/root/cybersec
ExecStart=/root/cybersec/.venv/bin/python cyber-panel/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Servisi başlatın ve etkinleştirin:
```bash
sudo systemctl daemon-reload
sudo systemctl start cybersec
sudo systemctl enable cybersec
```

Durumunu kontrol edin:
```bash
sudo systemctl status cybersec
```

Artık tarayıcınızdan **`http://SUNUCU_IP_ADRESINIZ:5000`** yazarak canlı sunucunuzdaki panele ve **%100 gerçek canlı ağ paket dinleyicisine** erişebilirsiniz! 🚀

---

## 🐳 Yöntem 3: Docker ve Host Network İle Çalıştırma

Eğer sunucunuzda **Docker** kurulu ise, sunucunun gerçek ağ kartını dinlemek için `--net=host` bayrağı ile tek komutta çalıştırabilirsiniz:

```bash
# Docker imajını derleyin
docker build -t cybersec-panel .

# Sunucu ağ kartına doğrudan bağlı (Raw Socket yetkili) container başlatın
docker run -d --name cyberpanel --net=host --privileged cybersec-panel
```

---

## 🔒 Ek Güvenlik İpuçları (Prodüksiyon Sunucuları İçin)
- **Güvenlik Duvarı (UFW):** Sadece ihtiyacınız olan portları açın: `sudo ufw allow 5000/tcp` veya Nginx arkasına alıyorsanız `sudo ufw allow 80/tcp`.
- **Nginx & SSL (HTTPS):** Let's Encrypt (`certbot`) kullanarak ücretsiz SSL sertifikası tanımlayabilir ve domain adınızla güvenli bağlantı kurabilirsiniz.

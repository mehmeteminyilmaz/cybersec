FROM python:3.11-slim

WORKDIR /app

# Bağımlılıkları kopyala ve yükle
COPY cyber-panel/requirements.txt /app/cyber-panel/requirements.txt
RUN pip install --no-cache-dir -r cyber-panel/requirements.txt pytest

# Tüm projeyi kopyala
COPY . /app

EXPOSE 5000

CMD ["python", "cyber-panel/app.py"]

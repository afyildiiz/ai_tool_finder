# Temel imaj olarak Python 3.x kullan
FROM python:3.11

# Çalışma dizinini ayarla
WORKDIR /app

# Bağımlılıkları kopyala ve yükle
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# Flask uygulamasını çalıştırmak için komut
CMD ["python", "app.py", "--host=0.0.0.0"]
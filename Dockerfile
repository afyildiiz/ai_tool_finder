# Temel imaj olarak Python 3.x kullan
FROM python:3.9-slim-buster

# Çalışma dizini oluştur
WORKDIR /app

# Gerekli bağımlılıkları kopyala
COPY requirements.txt requirements.txt

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# Uygulamanın çalışacağı portu belirt
EXPOSE 5000

# Uygulamayı başlat
CMD ["flask", "run", "--host=0.0.0.0"]
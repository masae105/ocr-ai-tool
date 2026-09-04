FROM python:3.13-slim

# Tesseract・日本語OCR・Popplerをインストール
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-jpn \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリ
WORKDIR /app

# Pythonパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトをコピー
COPY . .

# Renderから指定されたポートで起動
CMD gunicorn --bind 0.0.0.0:$PORT --timeout 300 app:app
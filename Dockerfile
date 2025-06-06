# Usa uma imagem base do Python 3.11 (uma versão leve do Linux com Python)
FROM python:3.11-slim

# Define o diretório de trabalho dentro do servidor
WORKDIR /app

# Instala os programas que nosso bot precisa (Tesseract, Português e Poppler)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    poppler-utils \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copia nosso arquivo de "lista de compras" do Python para o servidor
COPY requirements.txt .

# Instala as bibliotecas Python listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do nosso bot para o servidor
COPY bot_anny.py .

# Define o comando final que liga o bot quando o servidor iniciar
CMD ["python", "bot_anny.py"]
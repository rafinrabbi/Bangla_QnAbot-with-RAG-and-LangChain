FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential tesseract-ocr libglib2.0-0 libsm6 libxrender1 libxext6 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY . .

# Install supervisord
RUN pip install supervisor

# Expose both ports
EXPOSE 8000 7860

# Add supervisord config
COPY supervisord.conf /etc/supervisord.conf

CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisord.conf"]
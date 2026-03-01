FROM openjdk:17-slim

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p data/raw data/processed data/processed/models data/processed/results tableau/data

EXPOSE 8888 4040

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

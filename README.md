# Fugle Fast API
This project is a service for algorithmic trading of Taiwan stocks. It leverages the Fugle Python API library and FastAPI to provide a robust and efficient trading services.

# Features(In Progress)
- One stop API aggregation: integrate trading API and market API in one domain
- Integrate advance trading methods: iceberg order, stop loss/trailing profit order, swing trading
- Virtual Wallet: preventing users from defaulting on delivery obligations at T + 2
- Scalability: designed to scale with your trading needs.

# Getting Started
## Prerequisites
- Python 3.10
- Fugle's Trading credentials/Marketdata API Key

### Rename you p12 credential
```bash
mv filename.p12 cert.p12
```
- FastAPI
- Uvicorn


## Installation
Run in docker:

### Build an image
```bash
docker build -t fugle-fastapi:latest .
```

### Generate Keyring pass
This is the way fugle manage the credentials, only need to run once to get the cryptfile_pass.cfg
```bash
docker run -it --rm \
    -v $(pwd)/credentials:/root/.local/share/python_keyring \
    -v $(pwd)/config.ini:/app/config.ini:ro \
    -v $(pwd)/cert.p12:/app/cert.p12 \
    -v $(pwd)/.env:/app/.env:ro \
    fugle-fastapi:latest python index.py
```

### Host a server
```bash
docker run -p 8000:8000 --rm -d \
    -v $(pwd)/credentials/cryptfile_pass.cfg:/root/.local/share/python_keyring/cryptfile_pass.cfg:ro \
    -v $(pwd)/config.ini:/app/config.ini:ro \
    -v $(pwd)/cert.p12:/app/cert.p12 \
    -v $(pwd)/.env:/app/.env:ro \
    fugle-fastapi:latest
```

# Self Host API
You can see the API progress in
[Swagger Docs](https://fugle.lynxlinkage.com/docs)
# Taiwan Stock Algorithmic Trading Service
This project is a service for algorithmic trading of Taiwan stocks. It leverages the Fugle Python API library and FastAPI to provide a robust and efficient trading solution.

# Features
Algorithmic Trading: Implement complex trading strategies using algorithms.
Real-time Data: Fetch real-time stock data from Fugle.
FastAPI: Efficient and fast API service for handling trading operations.
Scalability: Designed to scale with your trading needs.

# Getting Started
## Prerequisites
Python 3.10
Fugle's Trading credentials/Marketdata API Key
FastAPI
Uvicorn

## Installation
Run in docker:

### Build an image
```bash
docker build -t fugle-fastapi:latest .
```

### Generate Keyring pass
This is the way fugle manage the credentials, only need to run once to get the cryptfile_pass.cfg
```bash
docker run -it --rm -v $(pwd)/credentials:/root/.local/share/python_keyring fugle-fastapi:latest python index.py
```

### Host a server
```bash
docker run -p 8000:8000 -d -v $(pwd)/credentials/cryptfile_pass.cfg:/root/.local/share/python_keyring/cryptfile_pass.cfg:ro --rm fugle-fastapi:latest
```

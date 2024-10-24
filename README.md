# Fugle Fast API

[![codecov](https://codecov.io/gh/yitech/fugle-fastapi/graph/badge.svg?token=ESEZZX1WSI)](https://codecov.io/gh/yitech/fugle-fastapi)

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


# For developer
## Local Run
```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

You can always use flake8 to make sure the coding quality

## Installation
```
pip install flake8 autopep8 black mypy
```

## Linting
```bash
pip install flake8 autopep8 black
flake8 app
```

Tools for auto reformatting:
```bash
autopep8 --select=W293 --in-place app/models/fugle.py
```

```bash
black app
```

## Type Checking
```bash
pip install mypy
mypy --ignore-missing-imports --check-untyped-defs app
```

## Unittest
```bash
pip install pytest httpx pytest-asyncio pytest-cov
pytest --cov=app --cov-report=html
```

## Generate Client Code
``` bash
openapi-generator-cli generate -c ./openapi_generator_config.json
```
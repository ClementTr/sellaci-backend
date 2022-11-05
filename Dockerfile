FROM python:3.7-alpine AS build-image

WORKDIR /app

COPY requirements.txt requirements.txt

# instruction to be run during imagedocker build
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y git python3-dev gcc --no-install-recommends && \
    python -m venv /root/venv && \
    pip install -r requirements.txt && \
    apt-get remove --purge git python3-dev gcc -y && \
    apt-get autoremove -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

FROM python:3.7-slim

COPY . .

EXPOSE 5000 

CMD ["python", "app.py"]

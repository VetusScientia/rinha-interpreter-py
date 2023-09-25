FROM python:3.9-ubuntu

WORKDIR /app

COPY src ./
COPY source.rinha.json /var/rinha/source.rinha.json
COPY requirements.txt ./

CMD ["python", "main.py", "-s", "/var/rinha/source.rinha.json"]

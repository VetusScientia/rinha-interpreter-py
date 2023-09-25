FROM python:3.9

WORKDIR /app

COPY src ./
COPY source.rinha.json /var/rinha/source.rinha.json
COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD ["python", "main.py", "-s", "/var/rinha/source.rinha.json"]

FROM python:3.9

WORKDIR /app

COPY src ./
COPY ./var/rinha/fib.rinha.json /var/rinha/fib.rinha.json
COPY requirements.txt ./

CMD ["python", "main.py", "-s", "/var/rinha/fib.rinha.json"]

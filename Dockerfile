# Use a imagem base do Python 3.9
FROM python:3.9

WORKDIR /app

COPY main.py utils.py requirements.txt ./
COPY source.rinha.json var/rinha/source.rinha.json

RUN pip install -r requirements.txt

CMD ["python", "main.py"]

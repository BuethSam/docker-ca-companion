FROM python:3.11-slim

WORKDIR /app

RUN pip install docker

COPY app.py .

ENTRYPOINT ["python", "app.py"]

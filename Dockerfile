FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd -m botuser

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

USER botuser

CMD ["python", "main.py"]
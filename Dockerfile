FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HEALTH_PORT=8080

WORKDIR /app

# Create non-root user for Kubernetes security best practices
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/sh appuser && \
    mkdir -p /data && chown -R appuser:appuser /app /data

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

USER 1000:1000
EXPOSE 8080

CMD ["python", "main.py"]

# ---------------------------------------------------------
# Stage 1: Build Environment & Python Dependencies
# ---------------------------------------------------------
FROM python:3.13-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------------------------------------------------------
# Stage 2: Minimal Production Runtime
# ---------------------------------------------------------
FROM python:3.13-slim AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Copy only installed wheels and libraries from builder
COPY --from=builder /install /usr/local

# Create non-privileged system user for runtime security
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m -s /bin/bash appuser

# Copy application source files
COPY app/ ./app/
COPY README.md .

# Change ownership of working files to appuser
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

# Health check to ensure service uptime
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
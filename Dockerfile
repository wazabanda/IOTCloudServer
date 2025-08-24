# syntax=docker/dockerfile:1
FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    # psycopg2 dependencies
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    # Pillow dependencies
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev \
    tcl-dev \
    harfbuzz-dev \
    fribidi-dev \
    # CFFI dependencies
    libffi-dev \
    # Cryptography dependencies
    openssl-dev \
    cargo \
    # Additional dependencies
    linux-headers

# Create a non-privileged user
RUN adduser -D -h /home/appuser -s /bin/sh appuser && \
    mkdir -p /app && \
    chown appuser:appuser /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Switch to non-privileged user
USER appuser

# Copy the application
COPY --chown=appuser:appuser . .

# Expose the port
EXPOSE 8016

# Run the application with Daphne
CMD ["sh", "-c", "\
    python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    python manage.py shell -c \"from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@admin.com', 'admin')\" && \
    daphne -b 0.0.0.0 -p 8016 IOTCloudServer.asgi:application --verbosity 2 \
"]

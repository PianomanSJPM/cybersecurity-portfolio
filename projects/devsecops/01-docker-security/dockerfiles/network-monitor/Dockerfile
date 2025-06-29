# Multi-stage build for secure network monitoring
FROM python:3.9-slim as builder

# Set build arguments with default values
ARG BUILD_DATE=unknown
ARG VCS_REF=unknown
ARG VERSION=1.0.0

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies globally
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-slim

# Set labels for better image management
LABEL maintainer="Stephen Miller <stephen.miller@example.com>"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.revision="${VCS_REF}"
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.title="Network Security Monitor"
LABEL org.opencontainers.image.description="Secure network monitoring container for DevSecOps"

# Install system dependencies for packet capture
RUN apt-get update && apt-get install -y \
    tcpdump \
    net-tools \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r security && useradd -r -g security security

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy application code
COPY network_monitor_simple.py .
COPY config/ ./config/
COPY modules/ ./modules/

# Create necessary directories
RUN mkdir -p /app/logs /app/reports /app/backups

# Set proper permissions
RUN chown -R security:security /app && \
    chmod -R 755 /app

# Switch to non-root user
USER security

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "network_monitor_simple.py"] 
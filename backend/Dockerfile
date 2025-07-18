# Menshun Backend - Multi-stage Docker Build
# This Dockerfile creates optimized images for development and production environments
# with comprehensive security, performance, and observability features

# =============================================================================
# Build Arguments
# =============================================================================
ARG PYTHON_VERSION=3.11
ARG BUILD_DATE
ARG VCS_REF

# =============================================================================
# Base Stage - Common Dependencies
# =============================================================================
FROM python:${PYTHON_VERSION}-slim as base

# Set build arguments as environment variables
ENV BUILD_DATE=${BUILD_DATE}
ENV VCS_REF=${VCS_REF}

# Set Python environment variables for optimal container behavior
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Build dependencies
    gcc \
    g++ \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    # Runtime dependencies
    curl \
    netcat-traditional \
    # Security tools
    ca-certificates \
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates

# Create non-root user for security
RUN groupadd -r menshun && useradd -r -g menshun -d /app -s /bin/bash menshun

# Create application directories
RUN mkdir -p /app/logs /app/vault_data /app/temp \
    && chown -R menshun:menshun /app

# =============================================================================
# Dependencies Stage - Install Python Dependencies
# =============================================================================
FROM base as dependencies

# Install pip and setuptools
RUN pip install --upgrade pip setuptools wheel

# Copy dependency files
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# =============================================================================
# Development Stage - Hot Reload and Development Tools
# =============================================================================
FROM dependencies as development

# Install development dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt

# Set development environment
ENV ENVIRONMENT=development \
    DEBUG=true \
    LOG_LEVEL=DEBUG

# Copy application code
WORKDIR /app
COPY --chown=menshun:menshun . .

# Install the application in development mode
RUN pip install -e .

# Health check script
COPY --chown=menshun:menshun scripts/health_check.py /app/health_check.py
RUN chmod +x /app/health_check.py

# Switch to non-root user
USER menshun

# Expose port
EXPOSE 8000

# Development command with hot reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "debug"]

# =============================================================================
# Production Dependencies Stage - Optimized for Production
# =============================================================================
FROM base as production-deps

# Install only production dependencies
RUN pip install --upgrade pip setuptools wheel
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip check  # Verify no dependency conflicts

# =============================================================================
# Production Stage - Optimized and Secure
# =============================================================================
FROM production-deps as production

# Production environment variables
ENV ENVIRONMENT=production \
    DEBUG=false \
    LOG_LEVEL=INFO \
    PYTHONPATH=/app \
    # Security
    PYTHONHASHSEED=random \
    # Performance
    PYTHONOPTIMIZE=1

# Copy application code with proper ownership
WORKDIR /app
COPY --chown=menshun:menshun app/ ./app/
COPY --chown=menshun:menshun alembic.ini pyproject.toml ./
COPY --chown=menshun:menshun alembic/ ./alembic/

# Copy configuration files
COPY --chown=menshun:menshun scripts/ ./scripts/
RUN chmod +x ./scripts/*.py ./scripts/*.sh

# Install the application
RUN pip install --no-deps .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python scripts/health_check.py || exit 1

# Security: Remove unnecessary packages and clean up
RUN apt-get update && apt-get remove -y gcc g++ \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create startup script
RUN echo '#!/bin/bash' > /app/start.sh && \
    echo 'set -e' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo 'echo "Starting Menshun Backend..."' >> /app/start.sh && \
    echo 'echo "Environment: $ENVIRONMENT"' >> /app/start.sh && \
    echo 'echo "Build Date: $BUILD_DATE"' >> /app/start.sh && \
    echo 'echo "VCS Ref: $VCS_REF"' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo '# Wait for database' >> /app/start.sh && \
    echo 'echo "Waiting for database connection..."' >> /app/start.sh && \
    echo 'python scripts/wait_for_db.py' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo '# Run database migrations' >> /app/start.sh && \
    echo 'echo "Running database migrations..."' >> /app/start.sh && \
    echo 'alembic upgrade head' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo '# Seed directory roles if needed' >> /app/start.sh && \
    echo 'echo "Seeding directory roles..."' >> /app/start.sh && \
    echo 'python -m app.scripts.seed_roles --if-empty' >> /app/start.sh && \
    echo '' >> /app/start.sh && \
    echo '# Start the application' >> /app/start.sh && \
    echo 'echo "Starting FastAPI server..."' >> /app/start.sh && \
    echo 'exec gunicorn app.main:app \' >> /app/start.sh && \
    echo '    --bind 0.0.0.0:8000 \' >> /app/start.sh && \
    echo '    --workers ${WORKERS:-4} \' >> /app/start.sh && \
    echo '    --worker-class uvicorn.workers.UvicornWorker \' >> /app/start.sh && \
    echo '    --worker-connections ${WORKER_CONNECTIONS:-1000} \' >> /app/start.sh && \
    echo '    --max-requests ${MAX_REQUESTS:-1000} \' >> /app/start.sh && \
    echo '    --max-requests-jitter ${MAX_REQUESTS_JITTER:-100} \' >> /app/start.sh && \
    echo '    --timeout ${TIMEOUT:-30} \' >> /app/start.sh && \
    echo '    --keep-alive ${KEEP_ALIVE:-5} \' >> /app/start.sh && \
    echo '    --log-level ${LOG_LEVEL:-info} \' >> /app/start.sh && \
    echo '    --access-logfile - \' >> /app/start.sh && \
    echo '    --error-logfile - \' >> /app/start.sh && \
    echo '    --capture-output \' >> /app/start.sh && \
    echo '    --enable-stdio-inheritance' >> /app/start.sh

RUN chmod +x /app/start.sh

# Switch to non-root user
USER menshun

# Expose port
EXPOSE 8000

# Labels for metadata and compliance
LABEL org.opencontainers.image.title="Menshun Backend" \
      org.opencontainers.image.description="Enterprise Privileged Access Management Backend" \
      org.opencontainers.image.version="${APP_VERSION:-1.0.0}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.vendor="Menshun Security" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.url="https://github.com/your-org/menshun" \
      org.opencontainers.image.documentation="https://docs.menshun.com" \
      org.opencontainers.image.source="https://github.com/your-org/menshun" \
      maintainer="security@company.com"

# Production startup command
CMD ["/app/start.sh"]

# =============================================================================
# Testing Stage - For CI/CD Pipeline
# =============================================================================
FROM development as testing

# Install testing dependencies
RUN pip install --no-cache-dir pytest pytest-cov pytest-asyncio pytest-mock httpx

# Copy test configuration
COPY pytest.ini tox.ini ./
COPY tests/ ./tests/

# Set testing environment
ENV ENVIRONMENT=testing \
    DATABASE_URL=sqlite:///test.db \
    REDIS_URL=redis://redis:6379/1

# Default command runs tests
CMD ["pytest", "--cov=app", "--cov-report=xml", "--cov-report=html", "--cov-report=term-missing"]
# Estágio de construção
FROM python:3.12-slim as builder

WORKDIR /app

# Instala dependências de sistema necessárias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Cria e ativa um ambiente virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"


#Update pip
RUN pip install --upgrade pip
# Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Estágio final ---
FROM python:3.12-slim

# Configurações de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    DOCKER_ENV=true

# Instala apenas o runtime necessário
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*
# Copia o ambiente virtual do estágio builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Cria usuário não-root
RUN useradd -m appuser && \
    mkdir -p /app && \
    chown appuser:appuser /app

WORKDIR /app

# Copia a aplicação
COPY --chown=appuser:appuser src/ ./src/

# Configura health check
HEALTHCHECK --interval=30s --timeout=10s \
    CMD curl -f http://localhost:8000/ || exit 1

# Porta exposta
EXPOSE 8000

# Muda para usuário não-root
USER appuser

# Entrypoint otimizado
COPY --chown=appuser:appuser entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
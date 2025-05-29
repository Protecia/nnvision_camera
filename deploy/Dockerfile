# =========================
# 🛠️ ÉTAPE 1 : Build + install des deps
# =========================
FROM python:3.13-slim AS builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  nano \
  ffmpeg \
  gcc \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY deploy/requirements.txt ./
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt


# =========================
# 🧼 ÉTAPE 2 : Image finale légère
# =========================
FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive

# Runtime-only deps (plus légers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Créer un utilisateur non-root
RUN adduser --disabled-password --gecos '' appuser

WORKDIR /App

# Copier ton code source
COPY src/ .
RUN chown -R appuser:appuser /App

# Changer l'utilisateur courant
USER appuser

# Copier uniquement ce qu’il faut depuis builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN echo "Building at $(date)"

RUN chmod +x start.sh

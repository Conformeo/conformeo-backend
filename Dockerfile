# backend/Dockerfile (mis à jour)
FROM python:3.13-slim

# Éviter les messages d'avertissement d'apt (optionnel)
ENV DEBIAN_FRONTEND=noninteractive

# Mettre à jour la liste des paquets et installer les dépendances système minimales
# (nécessaires à psycopg2, cryptography, etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       gcc \
       libffi-dev \
       libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .

EXPOSE 8000

# Commande de démarrage (en dev)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

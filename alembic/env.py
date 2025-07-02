# backend/alembic/env.py

import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 2) Maintenant on peut importer le fichier de configuration Pydantic
from app.core.config import settings


# 3) Importer la Base et les modèles pour que Alembic les connaisse
from app.db.session import Base
from app.models.user import User  # à adapter si tu as d'autres modèles
from app.db.base import Base  # target_metadata = Base.metadata

from app.db.base_class import Base           # ← metadata cible

# Import side-effects pour enregistrer les modèles …
import app.models  # noqa: F401  (processing, gdpr_action, link, etc.)

# 1) On ajoute le dossier racine du projet (contenant "app/") au PYTHONPATH
#    pour que Python puisse importer "app.core.config" et "app.db.session", etc.
#    Ici, cwd() est ".../backend", donc join avec ".." remonte à la racine du projet.
project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.insert(0, project_root)


# --- Suite de la configuration Alembic ---
config = context.config
# Charger la config des logs à partir de alembic.ini
fileConfig(config.config_file_name)

# 4) On remplace la clé "sqlalchemy.url" par la valeur string de DATABASE_URL
#    Note l'utilisation de str(...) pour être sûr de passer une valeur str
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

# 5) target_metadata sert à Alembic pour le autogenerate
target_metadata = Base.metadata


def run_migrations_offline():
    """
    Exécute les migrations en 'offline' (sans connexion directe).
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Exécute les migrations en 'online' (connexion directe).
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

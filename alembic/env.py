# backend/alembic/env.py
# ---------------------------------------------------------------------------

import sys
import os
from pathlib import Path
from logging.config import fileConfig

from alembic import context                 # ←  context est disponible ici
from sqlalchemy import engine_from_config, pool

# ── 1) Ajouter le répertoire racine du projet au PYTHONPATH ────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # …/backend/..
sys.path.insert(0, PROJECT_ROOT.as_posix())

# ── 2) Charger la configuration de l’app (URL BDD, etc.) ───────────────────
from app.core.config import settings

# ── 3) Importer la Base et déclarer le metadata pour Alembic ───────────────
from app.db.base_class import Base          # TOUTES les tables héritent de ça
target_metadata = Base.metadata

# ── 4) Enregistrer tous les modèles (side-effects) ─────────────────────────
import app.models            # noqa: F401  (importe tenant, user, site, etc.)

# ── 5) Config Alembic ──────────────────────────────────────────────────────
config = context.config
fileConfig(config.config_file_name)
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))


# ────────────────────────────────────────────────────────────────────────────
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,       # utile pour les changements de type
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
# ---------------------------------------------------------------------------

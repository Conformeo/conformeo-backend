"""seed gdpr_actions

Revision ID: fbafba26d5b0
Revises     : 4c0799a39102
Create Date : 2025-07-02 10:45:11.527494
"""
from __future__ import annotations

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# ──────────────────────────────
revision: str = "fbafba26d5b0"
down_revision: Union[str, None] = "4c0799a39102"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
# ──────────────────────────────

# ⚠️  on ré-emploie le type ENUM déjà créé par 4c0799a39102
actionscope = sa.Enum("ALL", "LEGAL_BASIS", name="actionscope", create_type=False)

gdpr_actions_tbl = sa.table(
    "gdpr_actions",
    sa.column("label",   sa.String),
    sa.column("article", sa.String),
    sa.column("scope",   actionscope),
)

ACTIONS: list[dict[str, str]] = [
    # BASE OBLIGATOIRE ---------------------------------------------------------
    {"label": "Tenir un registre des traitements",           "article": "Art. 30",       "scope": "ALL"},
    {"label": "Informer les personnes concernées",           "article": "Art. 13-14",    "scope": "ALL"},
    {"label": "Limiter la conservation des données",         "article": "Art. 5-1-e)",   "scope": "ALL"},
    {"label": "Mettre en place une AIPD au besoin",          "article": "Art. 35",       "scope": "ALL"},
    {"label": "Documenter une procédure de violation",       "article": "Art. 33-34",    "scope": "ALL"},
    {"label": "Nommer un DPO (si requis)",                   "article": "Art. 37",       "scope": "ALL"},
    {"label": "Mettre en place des clauses de confidentialité", "article": "Art. 28-3 b", "scope": "ALL"},
    {"label": "Documenter les modalités d’exercice des droits", "article": "Art. 12-15", "scope": "ALL"},
    {"label": "Vérifier la sécurité des sous-traitants",     "article": "Art. 28",       "scope": "ALL"},
    {"label": "Mettre en place une politique de conservation","article": "Art. 5-1 e)",  "scope": "ALL"},
    {"label": "Gérer les violations de données (procédure)", "article": "Art. 33-34",    "scope": "ALL"},
    {"label": "Former les collaborateurs",                   "article": "Art. 39-1 b",   "scope": "ALL"},
    # BASE LÉGALE --------------------------------------------------------------
    {"label": "Recueillir un consentement explicite",         "article": "Art. 7",        "scope": "LEGAL_BASIS"},
    {"label": "Permettre le retrait du consentement",         "article": "Art. 7-3",      "scope": "LEGAL_BASIS"},
    {"label": "Informer sur la base contractuelle",           "article": "Art. 6-1 b",    "scope": "LEGAL_BASIS"},
    {"label": "Mettre à jour les CGU / contrats",             "article": "Art. 6-1 b",    "scope": "LEGAL_BASIS"},
    {"label": "Justifier l’obligation légale applicable",     "article": "Art. 6-1 c",    "scope": "LEGAL_BASIS"},
    {"label": "Conserver les pièces justificatives légales",  "article": "Art. 6-1 c",    "scope": "LEGAL_BASIS"},
    {"label": "Documenter l’intérêt légitime (LIA / Balance)","article": "Art. 6-1 f",    "scope": "LEGAL_BASIS"},
    {"label": "Mettre à disposition la LIA sur demande",      "article": "Art. 6-1 f",    "scope": "LEGAL_BASIS"},
    # EXIGENCES SÉCURITÉ -------------------------------------------------------
    {"label": "Chiffrer les données sensibles au repos",      "article": "Art. 32",       "scope": "ALL"},
    {"label": "Chiffrer les transferts externes",             "article": "Art. 32",       "scope": "ALL"},
    {"label": "Mettre en place un contrôle d’accès",          "article": "Art. 32",       "scope": "ALL"},
    {"label": "Revoir les habilitations périodiquement",      "article": "Art. 32",       "scope": "ALL"},
    {"label": "Sauvegarder et tester la restauration",        "article": "Art. 32",       "scope": "ALL"},
    {"label": "Journaliser les accès aux données",            "article": "Art. 32-2 d",   "scope": "ALL"},
    {"label": "Gérer les correctifs de sécurité (patching)",  "article": "Art. 32",       "scope": "ALL"},
    {"label": "Signer des CT / BAA avec les sous-traitants",  "article": "Art. 28",       "scope": "ALL"},
    {"label": "Vérifier le transfert hors UE (clauses, BCR…)", "article": "Chap. V",      "scope": "ALL"},
    {"label": "Tester / auditer la sécurité",                 "article": "Art. 32-1 d",   "scope": "ALL"},
]

# --------------------------------------------------------------------------- #
def upgrade() -> None:
    """Insertion bulk des 30 actions RGPD."""
    op.bulk_insert(gdpr_actions_tbl, ACTIONS)

# --------------------------------------------------------------------------- #
def downgrade() -> None:
    """Supprime seulement les lignes insérées par le seed."""
    conn = op.get_bind()
    labels = [row["label"] for row in ACTIONS]

    # ANY(:array) = OK si on passe un ARRAY explicite
    conn.execute(
        sa.text("""
            DELETE FROM gdpr_actions
            WHERE label = ANY(:lbls)
        """),
        {"lbls": labels},            # SQLAlchemy les convertit en ARRAY PG
    )

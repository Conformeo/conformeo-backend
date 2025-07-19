"""seed rgpd_exigences

Revision ID: 9aacd3e34108
Revises: 5b9f5c7394df
Create Date: 2025-07-18 14:31:45.242282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer

# revision identifiers, used by Alembic.
revision: str = '9aacd3e34108'
down_revision: Union[str, None] = '5b9f5c7394df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    t = table(
        "rgpd_exigences",
        column("id", Integer),
        column("label", String),
    )

    op.bulk_insert(
        t,
        [
            {"id": 1,  "label": "Tenir un registre des activités de traitement"},
            {"id": 2,  "label": "Identifier et documenter les finalités"},
            {"id": 3,  "label": "Déterminer une base légale pour chaque traitement"},
            {"id": 4,  "label": "Informer les personnes (art. 12–14)"},
            {"id": 5,  "label": "Gérer le consentement de manière vérifiable"},
            {"id": 6,  "label": "Garantir les droits (accès, effacement, portabilité…)"},
            {"id": 7,  "label": "Prévoir une procédure de notification des violations"},
            {"id": 8,  "label": "Réaliser des AIPD / DPIA lorsque requis"},
            {"id": 9,  "label": "Désigner un DPO et publier ses coordonnées"},
            {"id": 10, "label": "Encadrer les sous-traitants par contrat"},
            {"id": 11, "label": "Définir et respecter des durées de conservation"},
            {"id": 12, "label": "Mettre en œuvre des mesures de sécurité adaptées"},
            {"id": 13, "label": "Journaliser et tracer les accès aux données"},
            {"id": 14, "label": "Chiffrer ou pseudonymiser les données sensibles"},
            {"id": 15, "label": "Appliquer la confidentialité par défaut"},
            {"id": 16, "label": "Intégrer la protection dès la conception"},
            {"id": 17, "label": "Former et sensibiliser le personnel"},
            {"id": 18, "label": "Tenir une documentation de conformité à jour"},
            {"id": 19, "label": "Mettre en place un processus d’exercice des droits"},
            {"id": 20, "label": "Sécuriser les transferts hors UE (SCC, BCR…)"},
            {"id": 21, "label": "Gérer les cookies et traceurs (consentement)"},
            {"id": 22, "label": "Mettre à jour politiques internes & chartes IT"},
            {"id": 23, "label": "Réaliser des audits de conformité réguliers"},
            {"id": 24, "label": "Documenter la minimisation des données collectées"},
            {"id": 25, "label": "Nommer un RSSI ou équivalent"},
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM rgpd_exigences;")
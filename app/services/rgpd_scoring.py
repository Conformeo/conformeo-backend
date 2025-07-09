from typing import List, Dict
from app.models.gdpr_action import GdprAction
from app.models.gdpr_action_answer import GdprActionAnswer
from sqlalchemy.orm import Session

def compute_score(details):
    # Implémente le calcul du score RGPD
    if not details:
        return 0
    total = len(details)
    conformes = sum(1 for d in details if d.answer == "oui")
    return int(100 * conformes / total) if total else 0

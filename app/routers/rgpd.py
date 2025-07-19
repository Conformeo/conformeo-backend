# app/api/v1/endpoints/rgpd.py
from datetime import date      #  ← AJOUTE-LE
from typing import List, Optional
from datetime import datetime, timezone


from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.rgpd_audit import RgpdAudit
from app.models.user import User
from app.schemas.rgpd_audit import RgpdAuditCreate, RgpdAuditRead  # noqa: E501
from app.core.security import get_current_active_user
from app.crud import crud_rgpd
from app.schemas.enums import AnswerEnum

router = APIRouter(prefix="/rgpd", tags=["RGPD"])

_ANS_MAP = {
    "conforme":        AnswerEnum.CONFORME,
    "non_conforme":    AnswerEnum.NON_CONFORME,
    "non_applicable":  AnswerEnum.NA,
    "na":              AnswerEnum.NA,
}

def _normalize_answers(audit: RgpdAuditCreate) -> RgpdAuditCreate:
    for item in audit.exigences:
        item.answer = _ANS_MAP[item.answer.lower()]
    return audit


# -------------------------------------------------------------------------
# AUDITS
# -------------------------------------------------------------------------


@router.get(
    "/audits/last",
    response_model=RgpdAuditRead,
    summary="Dernier audit RGPD (ou stub vide) de l’utilisateur courant",
)
def get_last_audit(
    *,
    user_id: Optional[int] = Query(
        None,
        description="(Optionnel – réservé admin) Forcer l’ID utilisateur concerné",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Renvoie le **dernier audit** pour l’utilisateur indiqué.

    - Par défaut (pas de *query‑param*) : utilisateur authentifié via Bearer token.
    - *user_id* renseigné : audits du compte ciblé (usage admin/batch).

    Lorsque **aucun audit** n’existe encore, on renvoie un *stub* conforme au
    schéma `RgpdAuditRead` afin d’éviter toute erreur 404/500 côté front.
    """

    uid = user_id or current_user.id

    audit = (
        db.query(RgpdAudit)
        .filter(RgpdAudit.user_id == uid)
        .order_by(RgpdAudit.created_at.desc())
        .first()
    )

    if audit:
        return audit

    # ------------------------------------------------------------------
    # Aucun audit → on renvoie un objet "stub" valide (toutes les clés
    # obligatoires du modèle sont renseignées avec des valeurs neutres).
    # ------------------------------------------------------------------
    now = datetime.now(timezone.utc)
    return RgpdAuditRead(
        id=0,
        user_id=uid,
        score=0,
        conforme=0,
        non_conforme=0,
        statut="VIDE",          # ⚠️ adapter si Enum stricte (ex. AuditStatus.VIDE)
        critical_ko=[],
        created_at=now,
        updated_at=now,
    )


@router.get(
    "/audits/timeline",
    response_model=List[RgpdAuditRead],
    summary="Timeline complète des audits (tri chronologique croissant)",
)
def get_audit_timeline(
    *,
    user_id: Optional[int] = Query(
        None,
        description="(Optionnel – réservé admin) Forcer l’ID utilisateur concerné",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Renvoie tous les audits de l’utilisateur (triés du plus ancien au plus récent)."""

    uid = user_id or current_user.id

    return (
        db.query(RgpdAudit)
        .filter(RgpdAudit.user_id == uid)
        .order_by(RgpdAudit.created_at.asc())
        .all()
    )


@router.post("/audits", response_model=RgpdAuditRead, status_code=201)
def create_audit(
    *,
    audit_in: RgpdAuditCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    audit_in = _normalize_answers(audit_in)

    data = audit_in.model_dump(exclude_unset=True)
    data["user_id"] = current_user.id
    # S’assure qu’un titre existe toujours
    data.setdefault("titre", f"Audit {date.today():%Y-%m-%d}")

    return crud_rgpd.create_audit(db, data)



@router.get(
    "/audits/{audit_id}",
    response_model=RgpdAuditRead,
    summary="Détail d’un audit RGPD",
)
def get_audit(
    *,
    audit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Renvoie le détail d’un audit s’il appartient à l’utilisateur courant."""
    audit = crud_rgpd.get_audit_by_id(db, audit_id)
    if not audit or audit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit introuvable.",
        )
    return audit


# -------------------------------------------------------------------------
# EXEMPLE D’EXTENSION – Statistiques par domaine
# -------------------------------------------------------------------------


@router.get(
    "/audits/{audit_id}/domains",
    summary="Répartition des exigences par domaine (stub)",
)
def get_domain_stats(
    *,
    audit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Stub : renvoie la répartition conforme / non conforme par domaine."""

    audit = crud_rgpd.get_audit_by_id(db, audit_id)
    if not audit or audit.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Audit introuvable.")

    return []  # TODO: implémenter la vraie logique

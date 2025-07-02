from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.gdpr_action import GdprActionRead
from app.crud import crud_gdpr_action

router = APIRouter()

# ───────── Catalogue complet ─────────
@router.get(
    "/actions/",                      # ← ***slash final obligatoire***
    response_model=List[GdprActionRead],
    summary="Catalogue complet des actions RGPD",
)
def list_actions(db: Session = Depends(get_db)):
    return crud_gdpr_action.get_all(db)

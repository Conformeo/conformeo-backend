from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.obligation import ObligationRead, ObligationCreate, ObligationUpdate
from app.crud import crud_obligation

router = APIRouter(prefix="/obligations", tags=["Obligations"])

@router.get("/", response_model=list[ObligationRead])
def get_obligations(user_id: int, db: Session = Depends(get_db)):
    """
    Liste toutes les obligations RGPD d'un utilisateur.
    """
    return crud_obligation.get_all_by_user(db, user_id)

@router.post("/", response_model=ObligationRead)
def create_obligation(obligation: ObligationCreate, db: Session = Depends(get_db)):
    """
    Crée une obligation RGPD pour un utilisateur.
    """
    return crud_obligation.create(db, obligation)

@router.put("/{obligation_id}", response_model=ObligationRead)
def update_obligation(obligation_id: int, obligation: ObligationUpdate, db: Session = Depends(get_db)):
    """
    Met à jour une obligation RGPD.
    """
    db_obj = crud_obligation.get(db, obligation_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Obligation non trouvée")
    return crud_obligation.update(db, db_obj, obligation)

@router.delete("/{obligation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_obligation(obligation_id: int, db: Session = Depends(get_db)):
    from app.crud.crud_obligation import delete  # (si tu n'as pas déjà la fonction)
    success = delete(db, obligation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Obligation non trouvée")
    return None
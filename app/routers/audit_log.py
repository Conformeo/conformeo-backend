from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogRead  # À créer si pas déjà fait
from app.dependencies.auth import get_current_active_admin, get_current_active_user
from app.models.user import User as UserModel

router = APIRouter(prefix="/auditlog", tags=["auditlog"])

@router.get("/", response_model=List[AuditLogRead])
def list_logs(
    db: Session = Depends(get_db),
    admin: UserModel = Depends(get_current_active_admin),
):
    # Filtrer par tenant si besoin
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.audit_log import AuditLogRead
from app.crud import crud_audit_log

router = APIRouter(prefix="/audit-logs", tags=["audit_logs"])

@router.get("/", response_model=list[AuditLogRead])
def list_logs(user_id: int, db: Session = Depends(get_db)):
    return crud_audit_log.list_by_user(db, user_id)

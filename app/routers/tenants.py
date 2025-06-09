from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.tenant import Tenant, TenantCreate, TenantUpdate
from app.models.tenant import Tenant as TenantModel
from app.db.session import get_db

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("/", response_model=Tenant)
def create_tenant(tenant_in: TenantCreate, db: Session = Depends(get_db)):
    tenant = TenantModel(**tenant_in.dict())
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant


@router.get("/", response_model=list[Tenant])
def list_tenants(db: Session = Depends(get_db)):
    return db.query(TenantModel).all()


@router.get("/{tenant_id}", response_model=Tenant)
def get_tenant(tenant_id: int, db: Session = Depends(get_db)):
    tenant = db.query(TenantModel).filter(TenantModel.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant


@router.put("/{tenant_id}", response_model=Tenant)
def update_tenant(
    tenant_id: int, tenant_in: TenantUpdate, db: Session = Depends(get_db)
):
    tenant = db.query(TenantModel).filter(TenantModel.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    for key, value in tenant_in.dict().items():
        setattr(tenant, key, value)
    db.commit()
    db.refresh(tenant)
    return tenant


@router.delete("/{tenant_id}", response_model=Tenant)
def delete_tenant(tenant_id: int, db: Session = Depends(get_db)):
    tenant = db.query(TenantModel).filter(TenantModel.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    db.delete(tenant)
    db.commit()
    return tenant

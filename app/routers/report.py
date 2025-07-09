from fastapi import APIRouter, Depends
from app.schemas.report import ReportRequest, ReportResponse

router = APIRouter(prefix="/api/report", tags=["rapport"])

@router.post("/conformity", response_model=ReportResponse)
def generate_conformity_report(data: ReportRequest, user=Depends(get_current_user)):
    # Compose le rapport synthétique ici, renvoie un objet/dict
    return {
        "company": data.company,
        "date": data.date,
        "score": data.score,
        "modules": data.modules,  # [{name: str, status: str}]
        "checklist": data.checklist,  # [str]
        "recommendations": data.recommendations,  # [str]
    }

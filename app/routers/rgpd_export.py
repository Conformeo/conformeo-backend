from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.dpo import Dpo
from app.models.obligation import Obligation
from app.models.register import Register
from io import BytesIO
from fpdf import FPDF

router = APIRouter(prefix="/rgpd", tags=["rgpd"])

@router.get("/export-pdf", response_class=StreamingResponse)
def export_pdf(user_id: int, db: Session = Depends(get_db)):
    # Récupérer toutes les infos utiles
    user = db.query(User).filter(User.id == user_id).first()
    dpo = db.query(Dpo).filter(Dpo.user_id == user_id).first()
    obligations = db.query(Obligation).filter(Obligation.user_id == user_id).all()
    registers = db.query(Register).filter(Register.user_id == user_id).all()

    # Construire le PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    pdf.cell(0, 10, f"Registre RGPD - {user.email}", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Délégué à la Protection des Données (DPO)", ln=1)
    if dpo:
        pdf.cell(0, 8, f"Nom : {dpo.nom}", ln=1)
        pdf.cell(0, 8, f"Email : {dpo.email}", ln=1)
        pdf.cell(0, 8, f"Téléphone : {dpo.telephone or '—'}", ln=1)
        pdf.cell(0, 8, f"Désignation : {dpo.designation_date or '—'}", ln=1)
        pdf.cell(0, 8, f"Statut : {'Externe' if dpo.is_external else 'Interne'}", ln=1)
    else:
        pdf.cell(0, 8, "Aucun DPO désigné", ln=1)

    pdf.ln(4)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, "Obligations RGPD", ln=1)
    pdf.set_font("Arial", size=11)
    if obligations:
        for ob in obligations:
            status = "OK" if ob.status else "À faire"
            last_update = ob.last_update.strftime('%d/%m/%Y') if ob.last_update else "-"
            pdf.cell(0, 8, f"- {ob.label} [{status}] (MAJ {last_update})", ln=1)
    else:
        pdf.cell(0, 8, "Aucune obligation déclarée", ln=1)

    pdf.ln(4)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, "Registre des traitements", ln=1)
    pdf.set_font("Arial", size=11)
    if registers:
        for reg in registers:
            pdf.cell(0, 8, f"- {reg.nom_traitement} / {reg.finalite or '—'} / {reg.base_legale or '—'}", ln=1)
    else:
        pdf.cell(0, 8, "Aucun traitement renseigné", ln=1)

    # Output as stream
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return StreamingResponse(pdf_output, media_type='application/pdf', headers={
        "Content-Disposition": f"attachment; filename=registre_rgpd_{user_id}.pdf"
    })

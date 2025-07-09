from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def build_rgpd_pdf(report_data: dict) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Rapport d'auto-évaluation RGPD")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 90, f"Score de conformité : {report_data['score']}%")
    c.drawString(50, height - 110, f"Points conformes : {report_data['conforme']} / {report_data['total']}")
    c.drawString(50, height - 130, f"Points non conformes : {report_data['non_conforme']}")

    y = height - 170
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Points critiques non conformes :")
    c.setFont("Helvetica", 11)
    y -= 20

    for ko in report_data["critical_ko"]:
        c.drawString(60, y, f"- {ko['label']} ({ko['answer']})")
        if ko.get("advice"):
            y -= 15
            c.drawString(75, y, f"⮡ {ko['advice']}")
        y -= 25
        if y < 100:
            c.showPage()
            y = height - 70

    c.setFont("Helvetica-Bold", 13)
    y -= 10
    c.drawString(50, y, "Détails des non-conformités :")
    c.setFont("Helvetica", 11)
    y -= 20
    for ko in report_data["ko"]:
        c.drawString(60, y, f"- {ko['label']} ({ko['answer']})")
        if ko.get("advice"):
            y -= 15
            c.drawString(75, y, f"⮡ {ko['advice']}")
        y -= 25
        if y < 100:
            c.showPage()
            y = height - 70

    c.save()
    buffer.seek(0)
    return buffer.read()

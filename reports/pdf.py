from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def build_simple_pdf_report(title: str, sections: dict) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50
    pdf.setTitle(title)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(40, y, title)
    y -= 30

    pdf.setFont("Helvetica", 10)

    for section_title, lines in sections.items():
        if y < 100:
            pdf.showPage()
            y = height - 50
            pdf.setFont("Helvetica", 10)

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(40, y, str(section_title))
        y -= 18

        pdf.setFont("Helvetica", 10)
        for line in lines:
            if y < 80:
                pdf.showPage()
                y = height - 50
                pdf.setFont("Helvetica", 10)

            pdf.drawString(50, y, str(line)[:110])
            y -= 14

        y -= 10

    pdf.save()
    buffer.seek(0)
    return buffer.read()

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from PyPDF2 import PdfReader, PdfWriter
import os, io
from typing import Dict
from utils.files import ensure_dir

def build_salary_pdf(path: str, data: Dict):
    ensure_dir(os.path.dirname(path))
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    textobject = c.beginText(20*mm, 270*mm)
    textobject.setFont('Helvetica', 12)
    textobject.textLine(f"Salary Slip - {data['year']}-{data['month']}")
    textobject.textLine("")
    for k in ['employee_id','name','cnp','hire_date','manager_name','base_salary','bonus_total','adjustment_total','gross_salary','working_days','vacation_days']:
        if k in data:
            textobject.textLine(f"{k.replace('_',' ').title()}: {data[k]}")
    c.drawText(textobject)
    c.showPage()
    c.save()
    # password protect
    unprotected_pdf = buffer.getvalue()
    reader = PdfReader(io.BytesIO(unprotected_pdf))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    password = data.get('cnp') or 'password'
    writer.encrypt(password)
    with open(path, 'wb') as f:
        writer.write(f)
    return path

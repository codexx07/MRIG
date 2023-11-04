import os
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import Color

# Define the light indigo color
light_indigo = Color(0.9, 0.9, 0.98)

def onFirstPage(canvas, doc, logo_path):
    canvas.saveState()
    canvas.setFillColor(light_indigo)
    canvas.rect(0, doc.pagesize[1] - 2 * inch, doc.pagesize[0], 2 * inch, stroke=0, fill=1)
    
    logo_width = 2 * inch
    logo_height = 2 * inch
    x = 0
    y = doc.pagesize[1] - logo_height
    canvas.drawImage(logo_path, x, y, width=logo_width, height=logo_height)

    canvas.setFont('Helvetica-Bold', 30)
    heading_x = doc.width / 2.0 + 0.9 * inch
    heading_y = doc.pagesize[1] - 1 * inch
    canvas.setFillColorRGB(0, 0, 0)
    canvas.drawCentredString(heading_x, heading_y, "X-Ray Report")
    canvas.restoreState()

def generate_pdf(patient_info_path, medical_data_path, image_path, logo_path):
    pdf_path = os.path.join(os.getcwd(), "output.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=3* inch, bottomMargin=inch)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='BoldStyle', parent=styles['Normal'], fontName='Helvetica-Bold'))

    # Load patient information from JSON file
    with open(patient_info_path, 'r') as file:
        patient_info = json.load(file)

    # Load medical data from JSON file
    with open(medical_data_path, 'r') as file:
        medical_data = json.load(file)

    # Create flowable content for the PDF
    flowables = []

    # Add patient information from the patient JSON file to the PDF
    for key in ['name', 'age', 'gender']:
        value = patient_info.get(key, '')
        flowables.append(Paragraph('<b>{}:</b> {}'.format(key.capitalize(), value), styles['Normal']))

    flowables.append(Spacer(1, 0.5 * inch))

    # Hardcoded findings and impression
    findings = "The proximal radio-ulnar and elbow joints are intact and display normal alignment without fractures, dislocations, or signs of degenerative changes on the X-ray."
    impression = "Radiological assessment reveals no abnormalities in the elbow region, suggesting no evident bone or joint pathology in the imaged area."

    # Add the hardcoded findings and impression to the PDF
    flowables.append(Paragraph('<b>Findings:</b>', styles['Heading4']))
    flowables.append(Paragraph(findings, styles['Normal']))
    flowables.append(Spacer(1, 0.5 * inch))
    flowables.append(Paragraph('<b>Impression:</b>', styles['Heading4']))
    flowables.append(Paragraph(impression, styles['Normal']))
    flowables.append(Spacer(1, 0.5 * inch))

    # Add medical data from the medical JSON file to the PDF, with keys in bold and values in normal text
    for key, value in medical_data.items():
        flowables.append(Paragraph('<b>{}:</b> {}'.format(key.capitalize(), value), styles['BoldStyle']))

    # Insert a page break to ensure the X-ray image is on the second page
    flowables.append(PageBreak())

    # Add the X-ray image on the second page
    flowables.append(Image(image_path, width=6 * inch, height=4.5 * inch))  # Adjusted for a typical X-ray image aspect ratio
    flowables.append(Spacer(1, 0.5 * inch))

    # Add the footer on the second page
    flowables.append(Paragraph('This is a computer-generated document, no signature is required.', styles['Normal']))

    # Build the document
    doc.build(flowables, onFirstPage=lambda canvas, doc: onFirstPage(canvas, doc, logo_path))

    return pdf_path

# Paths to the JSON files and other resources
patient_info_path = r"C:\Users\tanma\Downloads\input_json.json"
medical_data_path = r"C:\Users\tanma\Downloads\output_json.json"
image_path = r"C:\Users\tanma\OneDrive\Desktop\Xray scan templates\aaa867f71f0fedbd9cdadd08e62a17_big_gallery.jpeg"
logo_path = r"C:\Users\tanma\Downloads\logoXray.png"

# Generate the PDF
pdf_path = generate_pdf(patient_info_path, medical_data_path, image_path, logo_path)
print(f"PDF generated successfully at: {pdf_path}")





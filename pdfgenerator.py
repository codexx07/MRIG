import os
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import Color

# Define the lightest indigo color
lightest_indigo = Color(0.92, 0.92, 0.98)

def onFirstPage(canvas, doc, logo_path, patient_info):
    canvas.saveState()
    canvas.setFillColor(lightest_indigo)
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
    
    # Print patient information in the same line
    info_line = f"Name: {patient_info['name']}                       Age: {patient_info['age']}                          Gender: {patient_info['gender']}"
    y_position = heading_y - 1.5 * inch
    canvas.setFont('Helvetica-Bold', 12)
    canvas.drawString(1 * inch, y_position, info_line)
    
    # Extend the black line to touch the right edge of the page
    canvas.setLineWidth(2)  # Set the line width
    canvas.setStrokeColorRGB(0, 0, 0)  # Set the stroke color to black
    x1 = 0  # Start x-coordinate (left edge)
    x2 = doc.width + 150  # End x-coordinate (right edge)
    y = heading_y - 1.7 * inch
    canvas.line(x1, y, x2, y)
    
    canvas.restoreState()

def generate_pdf(patient_info_path, medical_data_path, image_path1, image_path2, image_path3, image_path4, logo_path):
    pdf_path = os.path.join(os.getcwd(), "static/output.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=3*inch, bottomMargin=inch)
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

    # Create the table data
    table_data = [['Parameters', 'Percentage']]
    for key, value in medical_data.items():
        table_data.append([key.capitalize(), value])

    # Define table style with black border and light indigo background color
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), lightest_indigo),
        ('BACKGROUND', (0, 1), (-1, -1), lightest_indigo),
        ('TEXTCOLOR', (0, 0), (-1, -1), (0, 0, 0)),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
    ]

    # Create the table and apply the style
    medical_data_table_obj = Table(table_data, style=table_style, colWidths=[4*inch, 2*inch])

    # Add the medical data table to the PDF
    flowables.append(medical_data_table_obj)

    # Insert a page break to ensure the X-ray images are on separate pages
    flowables.append(PageBreak())

    # Add X-ray images to the 2nd page with smaller size
    for image_path in [image_path1, image_path2]:
        flowables.append(Spacer(0, 0.25 * inch))  # Add a 0.25-inch gap
        flowables.append(Image(image_path, width=5 * inch, height=3 * inch))  # Adjusted size for the X-ray image

    # Insert another page break to create the 3rd page
    flowables.append(PageBreak())

    # Add smaller X-ray images to the 3rd page
    for image_path in [image_path3, image_path4]:
        flowables.append(Spacer(0, 0.25 * inch))  # Add a 0.25-inch gap
        flowables.append(Image(image_path, width=5 * inch, height=3 * inch))  # Adjusted size for the X-ray image

    # Add the red text with a slight right shift in the footer
    red_text = '<font color="red">Important Disclaimer: Please only seek guidance and professional medical advice from a certified and experienced medical professional.</font>'
    centered_paragraph = Paragraph(red_text, styles['Normal'])
    centered_paragraph.alignment = 1  # Center alignment
    centered_paragraph.spaceAfter = 0.15 * inch  # Add a 0.15-inch gap
    flowables.append(centered_paragraph)

    # Build the document
    doc.build(flowables, onFirstPage=lambda canvas, doc: onFirstPage(canvas, doc, logo_path, patient_info))

    return pdf_path

# Paths to the JSON files and other resources
if __name__ == "__main__":
    patient_info_path = "static/input.json"
    medical_data_path = "static/output.json"
    image_path1 = "static/outputs/aaa867f71f0fedbd9cdadd08e62a17_big_gallery.jpeg"
    image_path2 = "static/outputs/bar_graph.png"
    image_path3 = "static/outputs/speedometers.png"                        
    image_path4 = "static/media/logoXray.png"
    logo_path = "static/outputs/heatmap.png"

# Generate the PDF
    pdf_path = generate_pdf(patient_info_path, medical_data_path, image_path1, image_path2, image_path3, image_path4, logo_path)
    print(f"PDF generated successfully at: {pdf_path}")




















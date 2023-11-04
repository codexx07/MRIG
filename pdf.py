import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import Color

# Define the light indigo color
light_indigo = Color(0.9, 0.9, 0.98)

def onFirstPage(canvas, doc):
    canvas.saveState()
    # Set the background color for the header to light indigo
    canvas.setFillColor(light_indigo)
    # Draw a rectangle across the top with the light indigo background
    canvas.rect(0, doc.pagesize[1] - 2 * inch, doc.pagesize[0], 2 * inch, stroke=0, fill=1)
    
    # Logo in the top-left corner at the edge of the page
    logo_width = 2 * inch
    logo_height = 2 * inch
    # Coordinates for the logo (top-left corner of the logo image)
    x = 0  # x-coordinate at the very left edge of the page
    y = doc.pagesize[1] - logo_height  # y-coordinate at the top edge of the page
    canvas.drawImage(logo_path, x, y, width=logo_width, height=logo_height)

    # Heading shifted 0.9 inches to the right from the center
    canvas.setFont('Helvetica-Bold', 30)
    heading_x = doc.width / 2.0 + 0.9 * inch  # Center + 0.9 inch to the right
    heading_y = doc.pagesize[1] - 1 * inch  # Center of the colored header area
    canvas.setFillColorRGB(0, 0, 0)  # Set color to black for the text
    canvas.drawCentredString(heading_x, heading_y, "X-Ray Report")
    canvas.restoreState()

def generate_pdf(name, age, gender, findings, impression, image_path, logo_path):
    pdf_path = os.path.join(os.getcwd(), "output.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=3* inch, bottomMargin=inch)

    flowables = []

    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_bold = styles['Heading4']

    # Patient Information and other content
    flowables.append(Paragraph('<b>Name:</b> {}'.format(name), style_bold))
    flowables.append(Paragraph('<b>Age:</b> {}'.format(age), style_bold))
    flowables.append(Paragraph('<b>Gender:</b> {}'.format(gender), style_bold))
    flowables.append(Spacer(1, 0.5 * inch))

    flowables.append(Paragraph('<b>Findings:</b>', style_bold))
    flowables.append(Paragraph(findings, style_normal))
    flowables.append(Spacer(1, 0.5 * inch))

    flowables.append(Paragraph('<b>Impression:</b>', style_bold))
    flowables.append(Paragraph(impression, style_normal))
    flowables.append(PageBreak())

    # Add the X-ray image on the second page
    flowables.append(Image(image_path, width=6 * inch, height=3 * inch))

    # Add the footer
    flowables.append(Spacer(1, 0.5 * inch))
    flowables.append(Paragraph('This is a computer-generated document, no signature is required.', style_normal))

    # Build the document with the flowables and the onFirstPage function
    doc.build(flowables, onFirstPage=onFirstPage)

    return pdf_path

# Example usage
name = "Yashvi M. Patel"
age = "21"
gender = "Female"
findings = "The proximal radio-ulnar and elbow joints are intact and display normal alignment without fractures, dislocations, or signs of degenerative changes on the X-ray."
impression = "Radiological assessment reveals no abnormalities in the elbow region, suggesting no evident bone or joint pathology in the imaged area."
image_path = r"C:\Users\tanma\OneDrive\Desktop\Xray scan templates\aaa867f71f0fedbd9cdadd08e62a17_big_gallery.jpeg"
logo_path = r"C:\Users\tanma\Downloads\logoXray.png"

# Generate the PDF
pdf_path = generate_pdf(name, age, gender, findings, impression, image_path, logo_path)
print(f"PDF generated successfully at: {pdf_path}")
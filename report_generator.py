from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generate_pdf_report(transcript, reference_text, final_result, filler_stats):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Voice Based Concept Understanding Report")
    y -= 40

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Transcribed Explanation:")
    y -= 20
    c.setFont("Helvetica", 10)
    for line in split_text(transcript, 90):
        c.drawString(50, y, line)
        y -= 15

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Understanding Score: {final_result['overall_score']}/100")
    y -= 20
    c.drawString(50, y, f"Understanding Level: {final_result['understanding_level']}")
    y -= 30

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Semantic Similarity: {final_result['overall_score']/100}")
    y -= 15
    c.drawString(50, y, f"Filler Word Ratio: {filler_stats['filler_ratio']}")
    y -= 15
    c.drawString(50, y, f"Confidence (Energy): {final_result['rms_energy']}")

    c.save()
    buffer.seek(0)
    return buffer

def split_text(text, max_chars):
    words = text.split()
    lines, current = [], ""
    for word in words:
        if len(current) + len(word) + 1 <= max_chars:
            current += (" " if current else "") + word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines
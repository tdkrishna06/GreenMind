"""PDF diagnosis report generator."""
from __future__ import annotations
from datetime import datetime
from fpdf import FPDF


class Report(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(23, 91, 56)
        self.cell(0, 10, "GreenMind AI | Plant Health Report", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(190, 165, 120)
        self.line(10, 22, 200, 22)
        self.ln(4)


def create_report(prediction, facts: dict) -> bytes:
    """Build a concise PDF report from a completed diagnosis."""
    # Built-in Helvetica is Latin-1 only; retain a reliable PDF for all labels.
    clean = lambda text: str(text).encode("latin-1", "replace").decode("latin-1")
    pdf = Report()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(70, 70, 70)
    pdf.cell(0, 6, clean(f"Generated: {datetime.now().strftime('%d %b %Y, %H:%M')}"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(23, 91, 56)
    pdf.cell(0, 8, clean(f"Diagnosis: {prediction.label.replace('___', ' - ').replace('_', ' ')}"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(30, 30, 30)
    pdf.multi_cell(0, 6, clean(f"Confidence: {prediction.confidence:.1%} | Inference time: {prediction.inference_seconds:.2f}s\nPlant: {facts['plant']} | Severity: {facts['severity']}"))
    for title, value in (("Description", facts["description"]), ("Symptoms", facts["symptoms"]), ("Traditional remedy", facts["traditional_remedy"]), ("Organic remedy", facts["organic_remedy"]), ("Prevention", facts["prevention"])):
        pdf.ln(3); pdf.set_font("Helvetica", "B", 12); pdf.set_text_color(104, 65, 30); pdf.cell(0, 7, clean(title), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=10); pdf.set_text_color(30, 30, 30)
        lines = value if isinstance(value, list) else [value]
        for item in lines: pdf.multi_cell(0, 5, clean(f"- {item}"))
    pdf.ln(3); pdf.set_font("Helvetica", "I", 8); pdf.set_text_color(90, 90, 90); pdf.multi_cell(0, 4, clean(facts["note"]))
    return bytes(pdf.output())

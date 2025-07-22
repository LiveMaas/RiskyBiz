import matplotlib.pyplot as plt
import sys
import json
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd

def plot_risk_scores(agg_results, output_path):
    units = list(agg_results.keys())
    scores = [agg_results[unit]['score'] for unit in units]
    plt.figure(figsize=(10, 6))
    bars = plt.bar(units, scores, color='skyblue')
    plt.xlabel('Business Unit')
    plt.ylabel('Risk Score (0-100)')
    plt.title('Risk Score by Business Unit')
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for bar, score in zip(bars, scores):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2, str(score), ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig(str(output_path))
    plt.close()

def generate_pdf_report(agg_results, chart_path, pdf_path):
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    # Title
    elements.append(Paragraph('Risk Report by Business Unit', styles['Title']))
    elements.append(Spacer(1, 12))
    # Add bar chart
    elements.append(Image(str(chart_path), width=400, height=250))
    elements.append(Spacer(1, 12))
    # Summary Table
    data = [['Business Unit', 'Risk Score', 'Finding Count']]
    for unit, data_dict in agg_results.items():
        data.append([unit, data_dict['score'], len(data_dict['findings'])])
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    doc.build(elements)

def main():
    # Usage: python report_generator.py agg_results.json
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            agg_results = json.load(f)
    else:
        print('Please provide the path to the aggregated results JSON file.')
        sys.exit(1)
    chart_path = Path(__file__).parent.parent / 'reports/risk_by_biz_unit.png'
    pdf_path = Path(__file__).parent.parent / 'reports/output_pdfs/risk_report.pdf'
    plot_risk_scores(agg_results, chart_path)
    generate_pdf_report(agg_results, chart_path, pdf_path)
    print(f'Bar chart saved to {chart_path}')
    print(f'PDF report saved to {pdf_path}')

if __name__ == '__main__':
    main() 
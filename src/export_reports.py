"""
src/components/export_reports.py
High-Fidelity Executive PDF & CSV Export Generator.
Generates publication-grade PDF briefing reports via ReportLab and structured CSV datasets.
"""

import io
from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

from src.components.ai_insights import generate_executive_ai_summary, generate_replenishment_table

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and draw total page count and footer.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages: int):
        self.saveState()
        # Top subtle bar
        self.setFillColor(colors.HexColor("#4F46E5"))
        self.rect(36, letter[1] - 18, letter[0] - 72, 3, fill=1, stroke=0)
        
        # Bottom footer line & text
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(36, 32, letter[0] - 36, 32)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(36, 20, "RetailPulse Sales Intelligence Platform • Executive Demand Briefing")
        
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(letter[0] - 36, 20, page_str)
        self.restoreState()

def generate_executive_pdf(
    raw_df: pd.DataFrame,
    daily_df: pd.DataFrame,
    comparison_df: pd.DataFrame,
    eval_metrics: Dict[str, Any],
    filter_info: Optional[Dict[str, Any]] = None
) -> bytes:
    """
    Builds a professional multi-section executive PDF report in memory.
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=45
    )

    summary = generate_executive_ai_summary(raw_df, daily_df, comparison_df)
    replenishment_df = generate_replenishment_table(comparison_df, raw_df)
    now_str = datetime.now().strftime("%B %d, %Y - %H:%M")

    # Typography & Styles
    styles = getSampleStyleSheet()
    
    brand_style = ParagraphStyle(
        "BrandHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0F172A")
    )
    
    subhead_style = ParagraphStyle(
        "SubHeader",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#64748B")
    )
    
    section_h1 = ParagraphStyle(
        "SectionH1",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=10,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155")
    )
    
    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#1E293B")
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # 1. Document Header Banner
    story.append(Paragraph("<b>RETAILPULSE DEMAND &amp; FORECASTING REPORT</b>", brand_style))
    meta_text = f"Generated: {now_str} • Model: Random Forest Regressor (300 Trees) • Scope: {len(comparison_df)} SKUs"
    story.append(Paragraph(meta_text, subhead_style))
    story.append(Spacer(1, 12))

    # 2. Executive KPI Summary Grid (2x3 Table)
    kpi_data = [
        [
            Paragraph("<b>HISTORICAL REVENUE</b>", subhead_style),
            Paragraph("<b>HISTORICAL VOLUME</b>", subhead_style),
            Paragraph("<b>PREDICTED FESTIVE 7D DEMAND</b>", subhead_style)
        ],
        [
            Paragraph(f"<font size=12 color='#0F172A'><b>${summary['total_revenue']:,.2f}</b></font>", brand_style),
            Paragraph(f"<font size=12 color='#0F172A'><b>{summary['total_quantity']:,.0f} units</b></font>", brand_style),
            Paragraph(f"<font size=12 color='#4F46E5'><b>{summary['total_festive_7d']:,.1f} units</b></font>", brand_style)
        ],
        [
            Paragraph("<b>PROJECTED INCREMENTAL REV</b>", subhead_style),
            Paragraph("<b>NET 7D DEMAND SURGE</b>", subhead_style),
            Paragraph("<b>MODEL ACCURACY (HOLDOUT)</b>", subhead_style)
        ],
        [
            Paragraph(f"<font size=12 color='#059669'><b>+${summary['projected_incremental_rev']:,.2f}</b></font>", brand_style),
            Paragraph(f"<font size=12 color='#059669'><b>+{summary['diff_units']:,.1f} u ({summary['surge_pct']:+.1f}%)</b></font>", brand_style),
            Paragraph(f"<font size=12 color='#0F172A'><b>MAE: {eval_metrics['mae']:.2f} | R²: {eval_metrics['r2']:.3f}</b></font>", brand_style)
        ]
    ]

    kpi_table = Table(kpi_data, colWidths=[180, 180, 180])
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 14))

    # 3. Product-Level Forecast & Inventory Advisor Table
    story.append(Paragraph("<b>Next 7-Day Demand Forecast &amp; Inventory Vulnerability</b>", section_h1))
    
    headers = [
        Paragraph("<b>SKU</b>", table_cell_bold),
        Paragraph("<b>Product Description</b>", table_cell_bold),
        Paragraph("<b>Category</b>", table_cell_bold),
        Paragraph("<b>Normal 7D</b>", table_cell_bold),
        Paragraph("<b>Festive 7D</b>", table_cell_bold),
        Paragraph("<b>Surge Multiplier</b>", table_cell_bold),
        Paragraph("<b>Risk Rating</b>", table_cell_bold)
    ]
    
    table_rows = [headers]
    for _, r in replenishment_df.iterrows():
        risk_color = "#E11D48" if r["Stockout_Risk"] == "High" else ("#D97706" if r["Stockout_Risk"] == "Moderate" else "#059669")
        risk_cell = Paragraph(f"<font color='{risk_color}'><b>{r['Stockout_Risk']}</b></font>", table_cell)
        
        row = [
            Paragraph(str(r["StockCode"]), table_cell),
            Paragraph(str(r["Description"])[:34], table_cell),
            Paragraph(str(r.get("Category", "N/A")), table_cell),
            Paragraph(f"{r['Normal_Predicted_7D']:.1f}", table_cell),
            Paragraph(f"<b>{r['Festive_Predicted_7D']:.1f}</b>", table_cell),
            Paragraph(f"{r['Surge_Multiplier']:.2f}x ({r['Variation_%']:+.0f}%)", table_cell),
            risk_cell
        ]
        table_rows.append(row)

    forecast_table = Table(table_rows, colWidths=[40, 160, 95, 55, 55, 80, 55])
    forecast_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#CBD5E1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("ALIGN", (3, 0), (5, -1), "RIGHT")
    ]))
    story.append(forecast_table)
    story.append(Spacer(1, 14))

    # 4. Strategic AI Findings & Replenishment Advisor
    story.append(Paragraph("<b>Executive AI Analytical Insights</b>", section_h1))
    
    findings = [
        f"<b>Demand Surge Velocity:</b> The festive period reflects a <b>{summary['seasonal_daily_ratio']:.2f}x daily revenue multiplier</b> (${summary['festive_daily_rev']:,.0f}/day festive vs ${summary['normal_daily_rev']:,.0f}/day normal).",
        f"<b>Peak Surge Exposure:</b> <b>{summary['top_surge_sku']}</b> exhibits the highest projected holiday demand explosion (+{summary['top_surge_pct']:.1f}%), requiring proactive buffer inventory to avoid stockouts.",
        f"<b>Revenue Concentration:</b> The top 3 products account for <b>{summary['top3_share']:.1f}%</b> of total catalog revenue (lead product alone generates {summary['top1_share']:.1f}%). Prioritize procurement availability for these core revenue drivers.",
        f"<b>Total Projected Growth Opportunity:</b> Capturing full 7-day festive demand yields an estimated <b>+${summary['projected_incremental_rev']:,.2f}</b> in additional gross sales compared to normal operational levels."
    ]
    
    for f in findings:
        story.append(Paragraph(f"• {f}", body_style))
        story.append(Spacer(1, 3))
        
    story.append(Spacer(1, 10))

    # 5. Methodology & Operational Limitations
    story.append(Paragraph("<b>Analytical Methodology &amp; Educational Prototype Boundaries</b>", section_h1))
    disclaimer_text = (
        "This analysis utilizes a Random Forest Regressor trained on 10 SKUs across two distinct 61-day windows "
        "(April–May 2025 baseline and October–November 2025 festive). Holdout evaluation yields MAE of "
        f"{eval_metrics['mae']:.2f} units, RMSE of {eval_metrics['rmse']:.2f} units, and R² of {eval_metrics['r2']:.3f}. "
        "The scenario differences reflect observed historical seasonal contrasts within these sample periods; "
        "they do not prove causal festival attribution. Current inventory levels and vendor lead times are not recorded "
        "in the dataset; inventory multipliers represent demand-side ratio targets."
    )
    story.append(Paragraph(disclaimer_text, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    return buf.getvalue()

def get_csv_exports(
    raw_df: pd.DataFrame,
    comparison_df: pd.DataFrame
) -> Dict[str, bytes]:
    """
    Returns UTF-8 CSV bytes for filtered transactions and product demand forecasts.
    """
    transactions_csv = raw_df.to_csv(index=False).encode("utf-8")
    
    replenishment_df = generate_replenishment_table(comparison_df, raw_df)
    forecast_csv = replenishment_df.to_csv(index=False).encode("utf-8")
    
    return {
        "transactions_csv": transactions_csv,
        "forecast_csv": forecast_csv
    }

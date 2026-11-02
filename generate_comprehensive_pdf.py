"""
MATH502 Assignment 1 Comprehensive Solutions & Code Guide PDF Generator
German University in Cairo (GUC) - Faculty of IET
Students: Mazen Altelbany (64-12371) & Yahia Talaat (64-3581)
Instructor: Dr. Mohammad Shehab | TA: Eng. Bahaaeldin Ibrahim
"""

import os
import sys
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable, Preformatted
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and draw running headers and footers with 'Page X of Y'."""
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

    def draw_page_decorations(self, page_count):
        # Suppress running header/footer on cover page (page 1)
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 7.5)
            self.setFillColor(colors.HexColor('#475569'))
            
            # Running Header
            self.drawString(48, 755, "MATH502: Numerical Methods  |  Assignment 1 Comprehensive Solution & Code Guide")
            self.drawRightString(564, 755, "GUC — Faculty of IET")
            self.setStrokeColor(colors.HexColor('#cbd5e1'))
            self.setLineWidth(0.6)
            self.line(48, 748, 564, 748)
            
            # Running Footer
            self.line(48, 42, 564, 42)
            self.drawString(48, 30, "Mazen Altelbany (64-12371) & Yahia Talaat (64-3581)  |  Dr. Mohammad Shehab")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(564, 30, page_text)
            self.restoreState()

def build_pdf():
    out_dir = "MATH502_Assignment1_Submission"
    os.makedirs(out_dir, exist_ok=True)
    pdf_filename = os.path.join(out_dir, "MATH502_Assignment1_Solutions_and_Code_Guide.pdf")
    
    # Page setup: Letter (612 x 792 pt), margins: 48 pt left/right, 44 pt top/bottom -> Usable width = 516 pt
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=48,
        rightMargin=48,
        topMargin=44,
        bottomMargin=44,
        title="MATH502 Assignment 1 Comprehensive Solutions & Code Guide",
        author="Mazen Altelbany & Yahia Talaat",
        subject="MATH502 Numerical Methods Solutions and MATLAB Code Walkthrough",
        creator="MATLAB R2026a / ReportLab"
    )

    # Styles
    styles = getSampleStyleSheet()
    
    c_primary = colors.HexColor('#1e3a8a')    # Academic Navy
    c_secondary = colors.HexColor('#0d9488')  # Teal Accent
    c_dark = colors.HexColor('#0f172a')       # Charcoal Body Text
    c_slate = colors.HexColor('#475569')      # Muted Slate
    c_code_bg = colors.HexColor('#f8fafc')    # Very Light Gray-Blue for code
    c_code_border = colors.HexColor('#cbd5e1')# Subtle border for code blocks
    c_border = colors.HexColor('#e2e8f0')     # General Table Border
    c_callout_bg = colors.HexColor('#eff6ff') # Soft Blue Callout

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_primary,
        alignment=1,
        spaceAfter=5
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13.5,
        textColor=c_slate,
        alignment=1,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=c_secondary,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_dark,
        spaceAfter=4
    )

    code_font_style = ParagraphStyle(
        'CodeFont',
        fontName='Courier',
        fontSize=6.5,
        leading=8.2,
        textColor=colors.HexColor('#0f172a')
    )

    code_header_style = ParagraphStyle(
        'CodeHeader',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#1e3a8a')
    )

    table_hdr_style = ParagraphStyle(
        'TableHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.0,
        leading=8.8,
        textColor=c_dark
    )

    table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=table_cell_style,
        alignment=1
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Italic'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=9.5,
        textColor=c_slate,
        alignment=1,
        spaceBefore=3,
        spaceAfter=5
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1e3a8a')
    )

    def make_code_flowables(title, code_str, chunk_size=36):
        """Splits long scripts into manageable styled tables of <= chunk_size lines to prevent page overflow."""
        lines = code_str.strip().split('\n')
        flowables = []
        total_chunks = (len(lines) + chunk_size - 1) // chunk_size
        
        for idx in range(total_chunks):
            start = idx * chunk_size
            end = min(start + chunk_size, len(lines))
            chunk_lines = lines[start:end]
            chunk_text = '\n'.join(chunk_lines)
            
            sub_title = f"<b>Script:</b> <code>{title}</code> &nbsp;&nbsp;|&nbsp;&nbsp; <b>Part {idx+1} of {total_chunks}</b> (Lines {start+1}–{end})"
            hdr_para = Paragraph(sub_title, code_header_style)
            pre_f = Preformatted(chunk_text, code_font_style)
            
            t = Table([[hdr_para], [pre_f]], colWidths=[516])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
                ('BACKGROUND', (0,1), (-1,-1), c_code_bg),
                ('BOX', (0,0), (-1,-1), 0.75, c_code_border),
                ('LINEBELOW', (0,0), (-1,0), 0.75, c_code_border),
                ('TOPPADDING', (0,0), (-1,-1), 2.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                ('LEFTPADDING', (0,0), (-1,-1), 5),
                ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ]))
            flowables.append(t)
            if idx < total_chunks - 1:
                flowables.append(Spacer(1, 4))
        return flowables

    def load_script(filename):
        path = os.path.join(out_dir, filename)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return f"% Error: {filename} not found."

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE & TABLE OF CONTENTS
    # =========================================================================
    story.append(Spacer(1, 8))
    story.append(Paragraph("GERMAN UNIVERSITY IN CAIRO (GUC)", ParagraphStyle('UniHdr', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=c_primary, alignment=1)))
    story.append(Paragraph("Faculty of Information Engineering and Technology (IET)", ParagraphStyle('FacHdr', fontName='Helvetica', fontSize=10, leading=13, textColor=c_slate, alignment=1)))
    story.append(Paragraph("Department of Engineering Mathematics  |  Semester 5", ParagraphStyle('DeptHdr', fontName='Helvetica-Oblique', fontSize=8.5, leading=11, textColor=c_slate, alignment=1)))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=c_primary, spaceBefore=0, spaceAfter=12))
    
    story.append(Paragraph("MATH502: NUMERICAL METHODS", title_style))
    story.append(Paragraph("ASSIGNMENT 1 COMPREHENSIVE SOLUTIONS & MATLAB CODE GUIDE", ParagraphStyle('SubSub', parent=title_style, fontSize=13, leading=16, textColor=c_secondary)))
    story.append(Paragraph("Non-Linear Systems, Newton Interpolation, Diode Circuit Root-Finding, Vandermonde Ill-Conditioning, and Satellite Constellation Wireless Energy Harvesting", subtitle_style))
    story.append(Spacer(1, 8))
    
    # Metadata Table
    meta_data = [
        [Paragraph("<b>Course Instructor:</b>", body_style), Paragraph("Dr. Mohammad Shehab", body_style)],
        [Paragraph("<b>Teaching Assistant:</b>", body_style), Paragraph("Eng. Bahaaeldin Ibrahim (<code>bahaaeldin.ibrahim@guc.edu.eg</code>)", body_style)],
        [Paragraph("<b>Programming Language:</b>", body_style), Paragraph("MATLAB (MathWorks R2026a)", body_style)],
        [Paragraph("<b>Submission Date:</b>", body_style), Paragraph("November 6, 2026", body_style)],
        [Paragraph("<b>Student 1 (Author):</b>", body_style), Paragraph("<b>Mazen Altelbany</b> &nbsp;&nbsp;|&nbsp;&nbsp; <b>ID:</b> 64-12371 &nbsp;&nbsp;|&nbsp;&nbsp; <b>Tutorial:</b> T-01", body_style)],
        [Paragraph("<b>Student 2 (Partner):</b>", body_style), Paragraph("<b>Yahia Talaat</b> &nbsp;&nbsp;|&nbsp;&nbsp; <b>ID:</b> 64-3581 &nbsp;&nbsp;|&nbsp;&nbsp; <b>Tutorial:</b> T-02", body_style)],
    ]
    meta_table = Table(meta_data, colWidths=[130, 386])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f1f5f9')),
        ('BACKGROUND', (1,0), (1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Table of Contents
    story.append(Paragraph("<b>Table of Contents / Guide Outline:</b>", h2_style))
    toc_data = [
        [Paragraph("<b>Section</b>", table_hdr_style), Paragraph("<b>Topic / Problem Description</b>", table_hdr_style), Paragraph("<b>MATLAB Script</b>", table_hdr_style), Paragraph("<b>Key Built-In Functions</b>", table_hdr_style)],
        [Paragraph("Section 1", table_cell_center), Paragraph("Programming Language Justification & Setup", table_cell_style), Paragraph("—", table_cell_center), Paragraph("Language Rationale, IEEE 754", table_cell_style)],
        [Paragraph("Problem 1", table_cell_center), Paragraph("LORAN Radio Navigation Hyperbolic Solver", table_cell_style), Paragraph("<code>Problem1_LORAN.m</code>", table_cell_style), Paragraph("<code>det</code>, <code>norm</code>, backslash <code>\\</code>, <code>fsolve</code>", table_cell_style)],
        [Paragraph("Problem 2", table_cell_center), Paragraph("WSN RSSI Localization & Horner's Scheme", table_cell_style), Paragraph("<code>Problem2_RSSI.m</code>", table_cell_style), Paragraph("<code>polyfit</code>, <code>polyval</code>, nested loops", table_cell_style)],
        [Paragraph("Problem 3", table_cell_center), Paragraph("Diode KVL Root-Finding (Bisection & Secant)", table_cell_style), Paragraph("<code>Problem3_Diode_Bisection_Secant.m</code>", table_cell_style), Paragraph("<code>fzero</code>, anonymous functions <code>@</code>", table_cell_style)],
        [Paragraph("Problem 4", table_cell_center), Paragraph("Diode DC Newton-Raphson & Convergence", table_cell_style), Paragraph("<code>Problem4_Diode_Newton.m</code>", table_cell_style), Paragraph("Analytical derivative, convergence checks", table_cell_style)],
        [Paragraph("Problem 5", table_cell_center), Paragraph("Packet Latency & Vandermonde Ill-Conditioning", table_cell_style), Paragraph("<code>Problem5_Packet_Latency.m</code>", table_cell_style), Paragraph("<code>vander</code>, <code>cond</code>, <code>polyval</code>, backslash <code>\\</code>", table_cell_style)],
        [Paragraph("Problem 6", table_cell_center), Paragraph("Satellite Energy Harvesting (Analytical & Quadrature)", table_cell_style), Paragraph("<code>Problem6_Satellite_Energy_Harvesting.m</code>", table_cell_style), Paragraph("<code>trapz</code>, <code>rand</code>, <code>atan</code>, <code>linspace</code>", table_cell_style)],
        [Paragraph("Section 8", table_cell_center), Paragraph("Master Automation Runner & IDE Execution Guide", table_cell_style), Paragraph("<code>run_all.m</code>", table_cell_style), Paragraph("Sequential batch execution runner", table_cell_style)],
    ]
    toc_table = Table(toc_data, colWidths=[55, 175, 136, 150])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 1: PROGRAMMING LANGUAGE JUSTIFICATION
    # =========================================================================
    story.append(Paragraph("1. Programming Language Selection & Justification", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=5))
    
    p1_just = r"""
    <b>MATLAB (MathWorks R2026a)</b> was selected as the sole programming language for this assignment based on the following academic and technical criteria:
    <br/><br/>
    1. <b>Faculty of IET Academic Standard:</b> MATLAB is the standard computing environment across the German University in Cairo for engineering mathematics, signals, and communications courses. Using MATLAB ensures direct compatibility with the grading environment used by course instructors and teaching assistants.
    <br/>
    2. <b>High-Performance Native Linear Algebra:</b> Built-in matrix operations, including the highly optimized LAPACK-backed backslash operator (<code>\</code>) for solving linear systems ($J \Delta \mathbf{x} = -F$), determinant evaluation (<code>det</code>), vector 2-norm (<code>norm</code>), and polynomial operations (<code>polyfit</code>, <code>polyval</code>, <code>vander</code>) execute natively in C/Fortran with IEEE 754 double-precision arithmetic ($\sim 10^{-16}$).
    <br/>
    3. <b>Crash-Proof Compatibility:</b> Core numerical algorithms (such as the multidimensional Newton-Raphson scheme, divided differences, Horner's nested polynomial evaluation, bisection, secant, composite trapezoid, composite Simpson's 1/3, and Monte-Carlo integration) are implemented from first principles using standard vectorized MATLAB constructs. They run out-of-the-box on both base MATLAB licenses and advanced lab installations with toolboxes.
    <br/>
    4. <b>Independent Verification Toolset:</b> Advanced built-in functions (<code>fsolve</code>/residual norms for systems, <code>fzero</code> for scalar root-finding, <code>cond</code> for Vandermonde matrix condition numbers, and <code>trapz</code> for numerical quadrature) provide rigorous cross-validation for every hand-calculated and algorithmic result.
    """
    story.append(Paragraph(p1_just, body_style))
    story.append(Spacer(1, 6))

    # =========================================================================
    # PROBLEM 1: LORAN NAVIGATION SOLVER
    # =========================================================================
    story.append(Paragraph("2. Problem 1: LORAN Non-Linear System Navigation Solver", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=5))
    
    p1_desc = r"""
    <b>Problem Statement & Engineering Background:</b><br/>
    LORAN calculates a vessel's position $(x, y)$ by measuring the Time Difference of Arrival (TDOA) of pulsed radio signals emitted by pairs of synchronized transmitter stations. Because the locus of points with a constant distance difference to two foci forms a hyperbola, the boat's location lies at the simultaneous intersection of two hyperbolic curves:
    <br/><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<b>Equation 1:</b>&nbsp;&nbsp; <i>f</i><sub>1</sub>(<i>x</i>, <i>y</i>) = <i>x</i><sup>2</sup> / 186<sup>2</sup> - <i>y</i><sup>2</sup> / (300<sup>2</sup> - 186<sup>2</sup>) - 1 = <i>x</i><sup>2</sup> / 34,596 - <i>y</i><sup>2</sup> / 55,404 - 1 = 0
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<b>Equation 2:</b>&nbsp;&nbsp; <i>f</i><sub>2</sub>(<i>x</i>, <i>y</i>) = (<i>y</i> - 500)<sup>2</sup> / 279<sup>2</sup> - (<i>x</i> - 300)<sup>2</sup> / (500<sup>2</sup> - 279<sup>2</sup>) - 1 = (<i>y</i> - 500)<sup>2</sup> / 77,841 - (<i>x</i> - 300)<sup>2</sup> / 172,159 - 1 = 0
    <br/><br/>
    <b>Analytical Jacobian Matrix Derivation:</b><br/>
    The multidimensional Newton-Raphson scheme iteratively updates $\mathbf{x}_{k+1} = \mathbf{x}_k + \Delta \mathbf{x}_k$ by solving the 2&times;2 linear system $J(\mathbf{x}_k) \Delta \mathbf{x}_k = -F(\mathbf{x}_k)$. The analytical partial derivatives are:
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>J</i><sub>11</sub> = &part;<i>f</i><sub>1</sub> / &part;<i>x</i> = 2<i>x</i> / 34,596 = <i>x</i> / 17,298,&nbsp;&nbsp;&nbsp;&nbsp;
    <i>J</i><sub>12</sub> = &part;<i>f</i><sub>1</sub> / &part;<i>y</i> = -2<i>y</i> / 55,404 = -<i>y</i> / 27,702
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>J</i><sub>21</sub> = &part;<i>f</i><sub>2</sub> / &part;<i>x</i> = -2(<i>x</i> - 300) / 172,159,&nbsp;&nbsp;&nbsp;&nbsp;
    <i>J</i><sub>22</sub> = &part;<i>f</i><sub>2</sub> / &part;<i>y</i> = 2(<i>y</i> - 500) / 77,841
    """
    story.append(Paragraph(p1_desc, body_style))
    story.append(Spacer(1, 4))

    # Hand calculation details
    p1_hand = r"""
    <b>Part (a): Pen-and-Paper Manual Iterations (Detailed Step-by-Step):</b><br/>
    Starting from initial guess $\mathbf{x}_0 = (200, 200)^T$:
    <br/>
    • <b>Iteration 1:</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>f</i><sub>1</sub>(200, 200) = 200<sup>2</sup>/34596 - 200<sup>2</sup>/55404 - 1 = 1.156203 - 0.721969 - 1 = <b>-0.565767</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>f</i><sub>2</sub>(200, 200) = (200-500)<sup>2</sup>/77841 - (200-300)<sup>2</sup>/172159 - 1 = 1.156203 - 0.058086 - 1 = <b>+0.098117</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>J</i><sub>0</sub> = [[0.01156203, -0.00721970], [0.00116172, -0.00770802]] &rArr; det(<i>J</i><sub>0</sub>) = <b>-8.073312 &times; 10<sup>-5</sup></b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;Solving via Cramer's Rule: &Delta;<i>x</i><sub>0</sub> = +62.791030, &Delta;<i>y</i><sub>0</sub> = +22.192804 &rArr; <b>x</b><sub>1</sub> = (<b>262.791030</b>, <b>222.192804</b>)<sup><i>T</i></sup>
    <br/>
    • <b>Iteration 2:</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>f</i><sub>1</sub>(<b>x</b><sub>1</sub>) = +0.105075,&nbsp;&nbsp; <i>f</i><sub>2</sub>(<b>x</b><sub>1</sub>) = -0.016574<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>J</i><sub>1</sub> = [[0.01519199, -0.00802082], [0.00043226, -0.00713781]] &rArr; det(<i>J</i><sub>1</sub>) = <b>-1.049705 &times; 10<sup>-4</sup></b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;Solving via Cramer's Rule: &Delta;<i>x</i><sub>1</sub> = -8.411356, &Delta;<i>y</i><sub>1</sub> = -2.831433 &rArr; <b>x</b><sub>2</sub> = (<b>254.379674</b>, <b>219.361371</b>)<sup><i>T</i></sup>
    """
    story.append(Paragraph(p1_hand, body_style))
    story.append(Spacer(1, 4))

    # Problem 1 Convergence Table
    p1_table_data = [
        [Paragraph("<b>Iter k</b>", table_hdr_style), Paragraph("<b>x<sub>k</sub></b>", table_hdr_style), Paragraph("<b>y<sub>k</sub></b>", table_hdr_style), Paragraph("<b>||F(x<sub>k</sub>)||<sub>2</sub></b>", table_hdr_style), Paragraph("<b>||&Delta;x<sub>k</sub>||<sub>2</sub></b>", table_hdr_style), Paragraph("<b>Status / Verification</b>", table_hdr_style)],
        [Paragraph("0", table_cell_center), Paragraph("200.000000", table_cell_center), Paragraph("200.000000", table_cell_center), Paragraph("5.7421 &times; 10<sup>-1</sup>", table_cell_center), Paragraph("6.6598 &times; 10<sup>1</sup>", table_cell_center), Paragraph("Initial starting guess", table_cell_style)],
        [Paragraph("1", table_cell_center), Paragraph("262.791030", table_cell_center), Paragraph("222.192804", table_cell_center), Paragraph("1.0637 &times; 10<sup>-1</sup>", table_cell_center), Paragraph("8.8751 &times; 10<sup>0</sup>", table_cell_center), Paragraph("Hand iteration 1 verified", table_cell_style)],
        [Paragraph("2", table_cell_center), Paragraph("254.379674", table_cell_center), Paragraph("219.361371", table_cell_center), Paragraph("1.9252 &times; 10<sup>-3</sup>", table_cell_center), Paragraph("1.6756 &times; 10<sup>-1</sup>", table_cell_center), Paragraph("Hand iteration 2 verified", table_cell_style)],
        [Paragraph("3", table_cell_center), Paragraph("254.221177", table_cell_center), Paragraph("219.307011", table_cell_center), Paragraph("6.8141 &times; 10<sup>-7</sup>", table_cell_center), Paragraph("5.9235 &times; 10<sup>-5</sup>", table_cell_center), Paragraph("Quadratic error plunge", table_cell_style)],
        [Paragraph("4", table_cell_center), Paragraph("<b>254.221120</b>", table_cell_center), Paragraph("<b>219.306992</b>", table_cell_center), Paragraph("<b>8.5457 &times; 10<sup>-14</sup></b>", table_cell_center), Paragraph("<b>7.4295 &times; 10<sup>-12</sup></b>", table_cell_center), Paragraph("<b>Converged (tol &le; 10<sup>-8</sup>)</b>", table_cell_style)],
    ]
    t_p1 = Table(p1_table_data, colWidths=[45, 80, 80, 95, 95, 121])
    t_p1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_p1)
    story.append(Spacer(1, 4))

    # Figure 1
    if os.path.exists("figures/fig_problem1.png"):
        story.append(Image("figures/fig_problem1.png", width=420, height=170))
        story.append(Paragraph("<b>Figure 1:</b> LORAN hyperbolic transmitter geometry, intersection curves, and Newton-Raphson iteration trajectory.", caption_style))
    story.append(Spacer(1, 4))

    # Problem 1 Code & Walkthrough
    story.append(Paragraph("<b>Problem 1 MATLAB Implementation & Code Walkthrough:</b>", h2_style))
    p1_code = load_script("Problem1_LORAN.m")
    for f in make_code_flowables("Problem1_LORAN.m", p1_code, chunk_size=36):
        story.append(f)
        story.append(Spacer(1, 3))
        
    p1_walkthrough = r"""
    <b>Code Walkthrough & Algorithmic Design:</b><br/>
    • <b>Lines 14–27 (Geometry & Derivative Handles):</b> Constant focal terms are precomputed as scalar constants. Anonymous function handles <code>f1</code> and <code>f2</code> implement the non-linear vector $F(x, y)$, and <code>df1_dx</code> through <code>df2_dy</code> evaluate the exact analytical Jacobian entries without finite-difference approximation errors.
    <br/>
    • <b>Lines 32–79 (Manual Step Validation):</b> Evaluates $F(\mathbf{x}_0)$ and $J_0$ directly, calculates $\det(J_0)$, and applies Cramer's rule to replicate the exact hand-calculated steps for iterations 1 and 2, printing detailed intermediate outputs for grader verification.
    <br/>
    • <b>Lines 82–112 (Newton-Raphson Iterative Engine):</b> Uses a <code>for</code> loop with maximum 50 iterations. In each step, the linear system $J_k \Delta = -F_k$ is solved using MATLAB's robust backslash operator <code>J_k \ (-F_k)</code>. Convergence is checked using both $\Delta$ and residual norm: <code>norm(delta) < 1e-8 || norm(F_k) < 1e-8</code>.
    <br/>
    • <b>Lines 114–142 (Crash-Proof Verification):</b> Uses <code>exist('fsolve', 'file')</code> to check if the Optimization Toolbox is installed. If available (e.g. university lab machines), it cross-validates against <code>fsolve</code>; otherwise, it computes the exact residual norm $\|F(\mathbf{x}^*)\| = 8.55 \times 10^{-14}$, guaranteeing 100% crash-free execution on any machine.
    """
    story.append(Paragraph(p1_walkthrough, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PROBLEM 2: WSN RSSI INTERPOLATION & HORNER'S SCHEME
    # =========================================================================
    story.append(Paragraph("3. Problem 2: Wireless Sensor Network (WSN) RSSI Localization", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=5))
    
    p2_desc = r"""
    <b>Problem Statement & Engineering Background:</b><br/>
    In Wireless Sensor Networks (WSNs), Received Signal Strength Indicator (RSSI) measurements in dBm are widely used for distance estimation and node localization. A sensor node collects RSSI values at five calibrated distances:
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;Distance $d$ [m]: [1.0, 2.5, 4.0, 6.0, 8.0],&nbsp;&nbsp;&nbsp;&nbsp;RSSI $f(d)$ [dBm]: [-40.0, -47.0, -54.0, -60.0, -66.0]
    <br/><br/>
    <b>Part (a): Newton Divided Difference Formulation:</b><br/>
    The 4th-order Newton interpolating polynomial is $P_4(d) = b_0 + b_1(d-d_0) + b_2(d-d_0)(d-d_1) + b_3(d-d_0)(d-d_1)(d-d_2) + b_4(d-d_0)(d-d_1)(d-d_2)(d-d_3)$, where the coefficients $b_k$ are the top diagonal of the divided difference table:
    """
    story.append(Paragraph(p2_desc, body_style))
    story.append(Spacer(1, 4))

    # Divided Difference Table
    p2_table_data = [
        [Paragraph("<b>i</b>", table_hdr_style), Paragraph("<b>d<sub>i</sub> [m]</b>", table_hdr_style), Paragraph("<b>f[d<sub>i</sub>]</b>", table_hdr_style), Paragraph("<b>1st Difference</b>", table_hdr_style), Paragraph("<b>2nd Difference</b>", table_hdr_style), Paragraph("<b>3rd Difference</b>", table_hdr_style), Paragraph("<b>4th Difference</b>", table_hdr_style)],
        [Paragraph("0", table_cell_center), Paragraph("1.0", table_cell_center), Paragraph("<b>-40.000000</b>", table_cell_center), Paragraph("<b>-4.666667</b>", table_cell_center), Paragraph("<b>0.000000</b>", table_cell_center), Paragraph("<b>+0.095238</b>", table_cell_center), Paragraph("<b>-0.025974</b>", table_cell_center)],
        [Paragraph("1", table_cell_center), Paragraph("2.5", table_cell_center), Paragraph("-47.000000", table_cell_center), Paragraph("-4.666667", table_cell_center), Paragraph("+0.476190", table_cell_center), Paragraph("-0.086580", table_cell_center), Paragraph("—", table_cell_center)],
        [Paragraph("2", table_cell_center), Paragraph("4.0", table_cell_center), Paragraph("-54.000000", table_cell_center), Paragraph("-3.000000", table_cell_center), Paragraph("+0.000000", table_cell_center), Paragraph("—", table_cell_center), Paragraph("—", table_cell_center)],
        [Paragraph("3", table_cell_center), Paragraph("6.0", table_cell_center), Paragraph("-60.000000", table_cell_center), Paragraph("-3.000000", table_cell_center), Paragraph("—", table_cell_center), Paragraph("—", table_cell_center), Paragraph("—", table_cell_center)],
        [Paragraph("4", table_cell_center), Paragraph("8.0", table_cell_center), Paragraph("-66.000000", table_cell_center), Paragraph("—", table_cell_center), Paragraph("—", table_cell_center), Paragraph("—", table_cell_center), Paragraph("—", table_cell_center)],
    ]
    t_p2 = Table(p2_table_data, colWidths=[25, 60, 80, 85, 85, 85, 96])
    t_p2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_p2)
    story.append(Spacer(1, 4))

    # Part b & c explanation
    p2_parts = r"""
    <b>Part (b): Estimation at $d = 5.0\text{ m}$ & Physical Discrepancy Discussion:</b><br/>
    Evaluating $P_4(5.0)$:
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>P</i><sub>4</sub>(5) = -40 + (-4.6667)(4) + (0)(4)(2.5) + (0.095238)(4)(2.5)(1) + (-0.025974)(4)(2.5)(1)(-1) = <b>-57.4524 dBm</b> &approx; <b>-57.45 dBm</b>.
    <br/>
    • <b>Physical Discrepancy Analysis:</b> The actual lab measurement at 5 m was <b>-57.0 dBm</b> (difference = <b>0.45 dB</b>). This physical discrepancy occurs because RF signal propagation in real environments is governed by the log-distance path loss model overlaid with stochastic phenomena:
    <br/>
    1. <i>Multipath Fading:</i> Radio waves reflect off walls, ceilings, and floors, arriving at the receiver antenna with random phase shifts that constructively or destructively interfere.
    <br/>
    2. <i>Shadowing:</i> Dynamic obstacles and small furniture alter the direct line-of-sight path.
    <br/>
    3. <i>Transceiver Hardware Imperfections:</i> Thermal noise, antenna orientation mismatch, and ADC quantization in low-cost sensor chips create measurement variance that pure polynomial interpolation does not model.
    <br/><br/>
    <b>Part (c): Horner's Nested Scheme & Computational Complexity:</b><br/>
    To evaluate $P_4(d)$ efficiently on resource-constrained embedded microcontrollers, we nest the polynomial:
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>P</i><sub>4</sub>(<i>d</i>) = <i>b</i><sub>0</sub> + (<i>d</i> - <i>d</i><sub>0</sub>) [ <i>b</i><sub>1</sub> + (<i>d</i> - <i>d</i><sub>1</sub>) [ <i>b</i><sub>2</sub> + (<i>d</i> - <i>d</i><sub>2</sub>) [ <i>b</i><sub>3</sub> + <i>b</i><sub>4</sub>(<i>d</i> - <i>d</i><sub>3</sub>) ] ] ]
    <br/>
    • <b>Operation Count Comparison:</b> Evaluating the direct standard polynomial form $\sum a_k d^k$ requires <b>10 multiplications and 4 additions</b>. Horner's nested scheme requires only <b>4 multiplications and 4 additions</b>. This yields a <b>60% reduction in multiplications</b>, significantly reducing CPU instruction cycles and minimizing floating-point roundoff error accumulation.
    """
    story.append(Paragraph(p2_parts, body_style))
    story.append(Spacer(1, 4))

    # Figure 2
    if os.path.exists("figures/fig_problem2.png"):
        story.append(Image("figures/fig_problem2.png", width=420, height=170))
        story.append(Paragraph("<b>Figure 2:</b> WSN RSSI measurement points, 4th-degree Newton interpolating polynomial, and validation at 5.0 meters.", caption_style))
    story.append(Spacer(1, 4))

    # Problem 2 Code & Walkthrough
    story.append(Paragraph("<b>Problem 2 MATLAB Implementation & Code Walkthrough:</b>", h2_style))
    p2_code = load_script("Problem2_RSSI.m")
    for f in make_code_flowables("Problem2_RSSI.m", p2_code, chunk_size=36):
        story.append(f)
        story.append(Spacer(1, 3))
        
    p2_walkthrough = r"""
    <b>Code Walkthrough & Algorithmic Design:</b><br/>
    • <b>Lines 14–38 (Divided Difference Construction):</b> Allocates a 2D matrix <code>D</code> where column 1 contains measured RSSI values. A nested loop builds the divided difference table column by column: <code>D(i, j) = (D(i+1, j-1) - D(i, j-1)) / (d(i+j-1) - d(i))</code>.
    <br/>
    • <b>Lines 40–58 (Horner's Scheme Implementation):</b> Extracts coefficients $b = D(1, :)$. Evaluates the nested polynomial backwards (from $k=n$ down to 1), multiplying by $(d_{\text{val}} - d_{k-1})$ at each stage to achieve $O(n)$ complexity.
    <br/>
    • <b>Lines 60–75 (Built-In Cross-Check):</b> Compares against MATLAB's built-in <code>polyfit</code> and <code>polyval</code>, confirming zero discrepancy to machine precision.
    """
    story.append(Paragraph(p2_walkthrough, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PROBLEM 3: DIODE DC CIRCUIT ROOT-FINDING (BISECTION & SECANT)
    # =========================================================================
    story.append(Paragraph("4. Problem 3: Diode DC Circuit Non-Linear Analysis (Bisection & Secant)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=5))
    
    p3_desc = r"""
    <b>Problem Statement & Circuit Modeling:</b><br/>
    Consider a series DC circuit consisting of a constant voltage supply $V_s = 1.0\text{ V}$, a current-limiting resistor $R = 1000\ \Omega$, and a forward-biased silicon semiconductor diode. From Kirchhoff's Voltage Law (KVL): $V_s = IR + V_D$. Applying Shockley's ideal diode equation $I = I_s (e^{V_D / (n V_T)} - 1)$, we express the diode voltage as $V_D = n V_T \ln(I / I_s + 1)$. Combining equations yields the non-linear root-finding problem:
    <br/><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>f</i>(<i>I</i>) = <i>I R</i> + <i>n V</i><sub>T</sub> ln(<i>I</i> / <i>I</i><sub>s</sub> + 1) - <i>V</i><sub>s</sub> = 0
    <br/><br/>
    Parameters: $I_s = 10^{-12}\text{ A}$, $n = 1.5$, $V_T = 25.85\text{ mV} = 0.02585\text{ V}$, $R = 1000\ \Omega$, $V_s = 1.0\text{ V}$. Target tolerance: $\epsilon = 10^{-4}\text{ A}$ ($0.1\text{ mA}$).
    <br/><br/>
    <b>Initial Interval & Intermediate Value Theorem:</b><br/>
    Evaluating $f(I)$ at the boundaries of $[0, 5\text{ mA}]$:
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>f</i>(0) = 0 + <i>n V</i><sub>T</sub> ln(1) - 1.0 = <b>-1.0000 V</b> &lt; 0
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>f</i>(5 &times; 10<sup>-3</sup>) = (5 &times; 10<sup>-3</sup>)(1000) + 1.5(0.02585) ln(5 &times; 10<sup>-3</sup> / 10<sup>-12</sup> + 1) - 1.0 = 5.0 + 0.86595 - 1.0 = <b>+4.86595 V</b> &gt; 0
    <br/>
    Since $f(I)$ is continuous on $[0, 5\text{ mA}]$ and $f(0) \cdot f(5\text{ mA}) < 0$, the Intermediate Value Theorem (IVT) guarantees at least one real root in $[0, 5\text{ mA}]$.
    """
    story.append(Paragraph(p3_desc, body_style))
    story.append(Spacer(1, 4))

    # Bisection Table
    p3_bis_data = [
        [Paragraph("<b>Iter</b>", table_hdr_style), Paragraph("<b>a [mA]</b>", table_hdr_style), Paragraph("<b>b [mA]</b>", table_hdr_style), Paragraph("<b>c [mA]</b>", table_hdr_style), Paragraph("<b>(b - a)/2 [A]</b>", table_hdr_style), Paragraph("<b>f(c) [V]</b>", table_hdr_style), Paragraph("<b>Next Bracket</b>", table_hdr_style)],
        [Paragraph("1", table_cell_center), Paragraph("0.0000", table_cell_center), Paragraph("5.0000", table_cell_center), Paragraph("2.5000", table_cell_center), Paragraph("1.2500 &times; 10<sup>-3</sup>", table_cell_center), Paragraph("+2.3391", table_cell_center), Paragraph("[0, 2.5] mA", table_cell_style)],
        [Paragraph("2", table_cell_center), Paragraph("0.0000", table_cell_center), Paragraph("2.5000", table_cell_center), Paragraph("1.2500", table_cell_center), Paragraph("6.2500 &times; 10<sup>-4</sup>", table_cell_center), Paragraph("+1.0622", table_cell_center), Paragraph("[0, 1.25] mA", table_cell_style)],
        [Paragraph("3", table_cell_center), Paragraph("0.0000", table_cell_center), Paragraph("1.2500", table_cell_center), Paragraph("0.6250", table_cell_center), Paragraph("3.1250 &times; 10<sup>-4</sup>", table_cell_center), Paragraph("+0.4103", table_cell_center), Paragraph("[0, 0.625] mA", table_cell_style)],
        [Paragraph("4", table_cell_center), Paragraph("0.0000", table_cell_center), Paragraph("0.6250", table_cell_center), Paragraph("0.3125", table_cell_center), Paragraph("1.5625 &times; 10<sup>-4</sup>", table_cell_center), Paragraph("+0.0709", table_cell_center), Paragraph("[0, 0.3125] mA", table_cell_style)],
        [Paragraph("5", table_cell_center), Paragraph("0.0000", table_cell_center), Paragraph("0.3125", table_cell_center), Paragraph("<b>0.15625</b>", table_cell_center), Paragraph("<b>7.8125 &times; 10<sup>-5</sup></b>", table_cell_center), Paragraph("<b>-0.1122</b>", table_cell_center), Paragraph("<b>[0.15625, 0.3125] mA</b>", table_cell_style)],
    ]
    t_p3_bis = Table(p3_bis_data, colWidths=[35, 70, 70, 75, 85, 75, 106])
    t_p3_bis.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_p3_bis)
    story.append(Spacer(1, 4))

    # Bisection note
    p3_bis_note = r"""
    • <b>Bisection Convergence Analysis:</b> After 5 iterations, the maximum error bound is $(b - a)/2 = 7.8125 \times 10^{-5}\text{ A} < 10^{-4}\text{ A}$. The method terminates with the midpoint estimate $\hat{I}_5 = (0.15625 + 0.3125)/2 = <b>0.234375\text{ mA} \approx 0.2344\text{ mA}</b>. If an optional 6th iteration is evaluated, evaluating $f(0.234375\text{ mA}) \approx -0.0177\text{ V} < 0$ shifts the left bracket boundary to $a = 0.234375\text{ mA}$, producing the 6th bracket $[0.234375, 0.3125]\text{ mA}$, with midpoint $\hat{I}_6 = (0.234375 + 0.3125)/2 = <b>0.273438\text{ mA} \approx 0.2734\text{ mA}</b> and error bound $3.90625 \times 10^{-5}\text{ A}$.
    """
    story.append(Paragraph(p3_bis_note, body_style))
    story.append(Spacer(1, 4))

    # Secant Table
    p3_sec_data = [
        [Paragraph("<b>Iter k</b>", table_hdr_style), Paragraph("<b>x<sub>k-1</sub> [mA]</b>", table_hdr_style), Paragraph("<b>x<sub>k</sub> [mA]</b>", table_hdr_style), Paragraph("<b>x<sub>k+1</sub> [mA]</b>", table_hdr_style), Paragraph("<b>|x<sub>k+1</sub> - x<sub>k</sub>| [A]</b>", table_hdr_style), Paragraph("<b>f(x<sub>k+1</sub>) [V]</b>", table_hdr_style)],
        [Paragraph("1", table_cell_center), Paragraph("0.000000", table_cell_center), Paragraph("5.000000", table_cell_center), Paragraph("0.852377", table_cell_center), Paragraph("4.1476 &times; 10<sup>-3</sup>", table_cell_center), Paragraph("+6.4973 &times; 10<sup>-1</sup>", table_cell_center)],
        [Paragraph("2", table_cell_center), Paragraph("5.000000", table_cell_center), Paragraph("0.852377", table_cell_center), Paragraph("0.213220", table_cell_center), Paragraph("6.3916 &times; 10<sup>-4</sup>", table_cell_center), Paragraph("-4.3159 &times; 10<sup>-2</sup>", table_cell_center)],
        [Paragraph("3", table_cell_center), Paragraph("0.852377", table_cell_center), Paragraph("0.213220", table_cell_center), Paragraph("<b>0.253033</b>", table_cell_center), Paragraph("<b>3.9813 &times; 10<sup>-5</sup></b>", table_cell_center), Paragraph("<b>+3.2912 &times; 10<sup>-3</sup></b>", table_cell_center)],
    ]
    t_p3_sec = Table(p3_sec_data, colWidths=[40, 95, 95, 95, 95, 96])
    t_p3_sec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_p3_sec)
    story.append(Spacer(1, 4))

    p3_sec_note = r"""
    • <b>Secant Convergence Analysis:</b> The Secant method satisfies the step tolerance $|x_3 - x_2| = 3.9813 \times 10^{-5}\text{ A} < 10^{-4}\text{ A}$ in only <b>3 iterations</b>, estimating $I^* \approx 0.253033\text{ mA}$. Validating against MATLAB's built-in <code>fzero</code> yields $I^* = <b>0.250181\text{ mA}</b> = 2.501809 \times 10^{-4}\text{ A}$.
    """
    story.append(Paragraph(p3_sec_note, body_style))
    story.append(Spacer(1, 4))

    # Figure 3
    if os.path.exists("figures/fig_problem3.png"):
        story.append(Image("figures/fig_problem3.png", width=420, height=165))
        story.append(Paragraph("<b>Figure 3:</b> Diode non-linear function $f(I)$, zero crossing at $I^* = 0.2502\text{ mA}$, and bisection bracket narrowing.", caption_style))
    story.append(Spacer(1, 4))

    # Problem 3 Code & Walkthrough
    story.append(Paragraph("<b>Problem 3 MATLAB Implementation & Code Walkthrough:</b>", h2_style))
    p3_code = load_script("Problem3_Diode_Bisection_Secant.m")
    for f in make_code_flowables("Problem3_Diode_Bisection_Secant.m", p3_code, chunk_size=36):
        story.append(f)
        story.append(Spacer(1, 3))
        
    p3_walkthrough = r"""
    <b>Code Walkthrough & Algorithmic Design:</b><br/>
    • <b>Lines 14–26 (Anonymous Function Modeling):</b> Implements $f(I) = IR + nV_T \ln(I/I_s + 1) - V_s$. Performs bracket sign check $f(a) \cdot f(b) < 0$ to guarantee convergence before iteration starts.
    <br/>
    • <b>Lines 30–58 (Bisection Algorithm):</b> Employs a <code>while (b - a)/2 > tol</code> loop. Computes midpoint $c = (a+b)/2$, checks sign changes $f(a) \cdot f(c) < 0$, and halves the interval at each step. Logs iteration data into an array for formatted tabular printing.
    <br/>
    • <b>Lines 62–95 (Secant Method Engine):</b> Implements the two-point difference formula $x_{k+1} = x_k - f(x_k) (x_k - x_{k-1}) / (f(x_k) - f(x_{k-1}))$. Stopping condition is governed by step-size $|x_{k+1} - x_k| < \text{tol}$.
    <br/>
    • <b>Lines 98–115 (Validation with fzero):</b> Calls <code>fzero(f, [a_init, b_init])</code> to find the true root to machine precision, confirming bisection and secant errors are well within the required $10^{-4}\text{ A}$.
    """
    story.append(Paragraph(p3_walkthrough, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PROBLEM 4: DIODE CIRCUIT NEWTON-RAPHSON METHOD
    # =========================================================================
    story.append(Paragraph("5. Problem 4: Diode Circuit 1D Newton-Raphson Method", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=5))
    
    p4_desc = r"""
    <b>Mathematical Formulation & Analytical Derivative:</b><br/>
    Applying the one-dimensional Newton-Raphson method to $f(I) = IR + nV_T \ln(I/I_s + 1) - V_s$:
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>I</i><sub>k</sub> = <i>I</i><sub>k-1</sub> - <i>f</i>(<i>I</i><sub>k-1</sub>) / <i>f'</i>(<i>I</i><sub>k-1</sub>)
    <br/>
    Differentiating $f(I)$ with respect to $I$:
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>f'</i>(<i>I</i>) = <i>R</i> + <i>n V</i><sub>T</sub> / (<i>I</i> + <i>I</i><sub>s</sub>)
    <br/><br/>
    <b>Rigorous Conditions for Quadratic Convergence:</b><br/>
    Newton-Raphson achieves asymptotic quadratic convergence ($|e_k| \le M |e_{k-1}|^2$) because:
    <br/>
    1. <b>Function Smoothness:</b> The non-linear function $f(I)$ is infinitely differentiable ($C^\infty$) on the physical domain $I \ge 0$.
    <br/>
    2. <b>Simple Root Condition:</b> The root $I^*$ is simple because $f'(I^*) = R + nV_T/(I^* + I_s) \approx 1000 + 155 = <b>1155\ \Omega \ne 0</b>$.
    <br/>
    3. <b>Strict Lower Bound on Derivative:</b> For all physical currents $I \ge 0$, $f'(I) \ge R = 1000\ \Omega > 0$. This guarantees that the derivative is strictly positive and bounded away from zero across the entire physical range, eliminating any possibility of division-by-zero or horizontal tangent singularities.
    """
    story.append(Paragraph(p4_desc, body_style))
    story.append(Spacer(1, 4))

    # Correctly Indexed Table 6
    p4_table_data = [
        [Paragraph("<b>Initial Guess</b>", table_hdr_style), Paragraph("<b>k</b>", table_hdr_style), Paragraph("<b>I<sub>k-1</sub> [mA]</b>", table_hdr_style), Paragraph("<b>f(I<sub>k-1</sub>) [V]</b>", table_hdr_style), Paragraph("<b>f'(I<sub>k-1</sub>) [&Omega;]</b>", table_hdr_style), Paragraph("<b>|&Delta;I<sub>k</sub>| [A]</b>", table_hdr_style), Paragraph("<b>I<sub>k</sub> [mA]</b>", table_hdr_style)],
        [Paragraph("<b>(a) I<sub>0</sub> = 0.35 mA</b><br/>(close to root)", table_cell_style), Paragraph("1", table_cell_center), Paragraph("0.350000", table_cell_center), Paragraph("+1.1251 &times; 10<sup>-1</sup>", table_cell_center), Paragraph("1.1108 &times; 10<sup>3</sup>", table_cell_center), Paragraph("1.0129 &times; 10<sup>-4</sup>", table_cell_center), Paragraph("0.248710", table_cell_center)],
        [Paragraph("", table_cell_style), Paragraph("2", table_cell_center), Paragraph("0.248710", table_cell_center), Paragraph("-1.7011 &times; 10<sup>-3</sup>", table_cell_center), Paragraph("1.1559 &times; 10<sup>3</sup>", table_cell_center), Paragraph("<b>1.4717 &times; 10<sup>-6</sup></b>", table_cell_center), Paragraph("<b>0.250181</b>", table_cell_center)],
        [Paragraph("<b>(b) I<sub>0</sub> = 1.00 mA</b><br/>(far from root)", table_cell_style), Paragraph("1", table_cell_center), Paragraph("1.000000", table_cell_center), Paragraph("+8.0354 &times; 10<sup>-1</sup>", table_cell_center), Paragraph("1.0388 &times; 10<sup>3</sup>", table_cell_center), Paragraph("7.7355 &times; 10<sup>-4</sup>", table_cell_center), Paragraph("0.226450", table_cell_center)],
        [Paragraph("", table_cell_style), Paragraph("2", table_cell_center), Paragraph("0.226450", table_cell_center), Paragraph("-2.7595 &times; 10<sup>-2</sup>", table_cell_center), Paragraph("1.1712 &times; 10<sup>3</sup>", table_cell_center), Paragraph("<b>2.3561 &times; 10<sup>-5</sup></b>", table_cell_center), Paragraph("<b>0.250011</b>", table_cell_center)],
    ]
    t_p4 = Table(p4_table_data, colWidths=[105, 25, 75, 80, 75, 76, 80])
    t_p4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_p4)
    story.append(Spacer(1, 4))

    # Table 7 Comparison
    p4_comp_data = [
        [Paragraph("<b>Method</b>", table_hdr_style), Paragraph("<b>Initial Conditions</b>", table_hdr_style), Paragraph("<b>Iterations</b>", table_hdr_style), Paragraph("<b>Final Root [mA]</b>", table_hdr_style), Paragraph("<b>Residual |f(I)| [V]</b>", table_hdr_style), Paragraph("<b>Convergence Rate</b>", table_hdr_style)],
        [Paragraph("Bisection", table_cell_style), Paragraph("[0, 5 mA]", table_cell_center), Paragraph("5", table_cell_center), Paragraph("0.234375", table_cell_center), Paragraph("1.1218 &times; 10<sup>-1</sup>", table_cell_center), Paragraph("Linear (r = 1)", table_cell_style)],
        [Paragraph("Secant", table_cell_style), Paragraph("x0=0, x1=5 mA", table_cell_center), Paragraph("3", table_cell_center), Paragraph("0.253033", table_cell_center), Paragraph("3.2912 &times; 10<sup>-3</sup>", table_cell_center), Paragraph("Superlinear (r &approx; 1.62)", table_cell_style)],
        [Paragraph("Newton-Raphson (a)", table_cell_style), Paragraph("I0 = 0.35 mA", table_cell_center), Paragraph("<b>2</b>", table_cell_center), Paragraph("<b>0.250181</b>", table_cell_center), Paragraph("<b>1.70 &times; 10<sup>-6</sup></b>", table_cell_center), Paragraph("<b>Quadratic (r = 2)</b>", table_cell_style)],
        [Paragraph("Newton-Raphson (b)", table_cell_style), Paragraph("I0 = 1.00 mA", table_cell_center), Paragraph("<b>2</b>", table_cell_center), Paragraph("<b>0.250011</b>", table_cell_center), Paragraph("<b>1.96 &times; 10<sup>-4</sup></b>", table_cell_center), Paragraph("<b>Quadratic (r = 2)</b>", table_cell_style)],
    ]
    t_p4_comp = Table(p4_comp_data, colWidths=[100, 85, 55, 80, 96, 100])
    t_p4_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_p4_comp)
    story.append(Spacer(1, 4))

    # Circuit operating point verification
    p4_phys = r"""
    • <b>Physical Circuit Verification:</b> The converged current $I^* \approx 0.250181\text{ mA}$ produces a resistor voltage drop $V_R = I^* R = (0.250181 \times 10^{-3})(1000) = <b>0.2502\text{ V}</b>. The remaining voltage drop across the diode is $V_D = V_s - V_R = 1.0 - 0.2502 = <b>0.7498\text{ V}</b>, exactly matching the typical physical forward voltage drop ($\sim 0.7\text{ V} - 0.75\text{ V}$) for a silicon diode in conduction.
    """
    story.append(Paragraph(p4_phys, body_style))
    story.append(Spacer(1, 4))

    # Figure 4
    if os.path.exists("figures/fig_problem4.png"):
        story.append(Image("figures/fig_problem4.png", width=420, height=165))
        story.append(Paragraph("<b>Figure 4:</b> Iterative convergence trajectories of Newton-Raphson method starting from $I_0 = 0.35\text{ mA}$ and $I_0 = 1.00\text{ mA}$.", caption_style))
    story.append(Spacer(1, 4))

    # Problem 4 Code & Walkthrough
    story.append(Paragraph("<b>Problem 4 MATLAB Implementation & Code Walkthrough:</b>", h2_style))
    p4_code = load_script("Problem4_Diode_Newton.m")
    for f in make_code_flowables("Problem4_Diode_Newton.m", p4_code, chunk_size=36):
        story.append(f)
        story.append(Spacer(1, 3))
        
    p4_walkthrough = r"""
    <b>Code Walkthrough & Algorithmic Design:</b><br/>
    • <b>Lines 14–22 (Derivative Modeling):</b> Sets up anonymous function handles for $f(I)$ and its exact analytical derivative $f'(I) = R + nV_T/(I + I_s)$.
    <br/>
    • <b>Lines 26–65 (Newton Execution Loop):</b> Iterates over each initial guess ($I_0 = 0.35\text{ mA}$ and $I_0 = 1.00\text{ mA}$). In each iteration, computes step $\Delta I = f(I) / f'(I)$, updates $I_{k} = I_{k-1} - \Delta I$, and checks termination condition $|\Delta I| < 10^{-4}\text{ A}$.
    <br/>
    • <b>Lines 68–80 (Comparative Method Summary):</b> Compares iteration counts, residuals, and asymptotic convergence orders against Bisection and Secant methods.
    """
    story.append(Paragraph(p4_walkthrough, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PROBLEM 5: PACKET LATENCY VANDERMONDE ILL-CONDITIONING
    # =========================================================================
    story.append(Paragraph("6. Problem 5: Packet Latency Vandermonde Interpolation & Ill-Conditioning", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=5))
    
    p5_desc = r"""
    <b>Problem Statement & Experimental Data:</b><br/>
    Network telemetry measures packet transmission latency $L(x)$ [ms] as a function of packet size $x$ [kB]:
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;Packet size $x$ [kB]: [150.0, 200.0, 230.0, 260.0, 300.0, 340.0, 400.0]
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;Latency $y$ [ms]: [2.10, 2.85, 3.35, 3.95, 4.90, 6.10, 8.05]
    <br/><br/>
    <b>Part (a): Vandermonde Matrix Formulation & Ill-Conditioning:</b><br/>
    With 7 distinct points, the unique interpolating polynomial has degree 6: $L(x) = \sum_{j=0}^6 c_j x^j$. Setting up the linear system $V \mathbf{c} = \mathbf{y}$, where $V_{i, j} = x_i^{7-j}$:
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>c</i><sub>6</sub> = -1.89262707 &times; 10<sup>-13</sup>,&nbsp;&nbsp;&nbsp;&nbsp;
    <i>c</i><sub>5</sub> = +3.01018087 &times; 10<sup>-10</sup>,&nbsp;&nbsp;&nbsp;&nbsp;
    <i>c</i><sub>4</sub> = -1.96580005 &times; 10<sup>-7</sup>
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>c</i><sub>3</sub> = +6.75374182 &times; 10<sup>-5</sup>,&nbsp;&nbsp;&nbsp;&nbsp;
    <i>c</i><sub>2</sub> = -1.28304368 &times; 10<sup>-2</sup>,&nbsp;&nbsp;&nbsp;&nbsp;
    <i>c</i><sub>1</sub> = +1.28842461 &times; 10<sup>0</sup>,&nbsp;&nbsp;&nbsp;&nbsp;
    <i>c</i><sub>0</sub> = -5.16017635 &times; 10<sup>1</sup>
    <br/><br/>
    <b>Condition Number & Error Magnification Analysis:</b><br/>
    The 2-norm condition number computed by MATLAB is <b>cond(V) = 2.2646 &times; 10<sup>19</sup></b>. In IEEE 754 double precision (machine epsilon $\varepsilon_{\text{mach}} \approx 2.22 \times 10^{-16}$), the theoretical upper bound on relative output error amplification is:
    <br/>
    $$\text{cond}(V) \cdot \varepsilon_{\text{mach}} \approx (2.2646 \times 10^{19}) \cdot (2.2204 \times 10^{-16}) \approx 5.028 \times 10^3 = 5028 \gg 1\ (502,800\%)$$
    Because this error amplification bound far exceeds 100%, roundoff errors in the right-hand vector are magnified by over <b>three orders of magnitude</b>. Consequently, the high-degree monomial coefficients lose all significant decimal digits, rendering high-degree Vandermonde systems mathematically and numerically catastrophic.
    <br/><br/>
    <b>Part (b): Evaluating at $x = 3.0\text{ kB}$ & Physical Extrapolation Breakdown:</b><br/>
    Evaluating $L(3.0)$:
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>L</i>(3.0) = <i>c</i><sub>6</sub>(3)<sup>6</sup> + <i>c</i><sub>5</sub>(3)<sup>5</sup> + ... + <i>c</i><sub>1</sub>(3) + <i>c</i><sub>0</sub> = <b>-47.850156 ms</b> &approx; <b>-47.85 ms</b>.
    <br/>
    • <b>Physical Impossibility:</b> In computer networking, packet latency consists of propagation delay ($d / v$), transmission/serialization delay ($x / R_{\text{link}}$), processing delay, and queueing delay. Every one of these physical components is strictly non-negative ($L > 0$). A negative latency of $-47.85\text{ ms}$ would violate causality (the packet would arrive before it was transmitted).
    <br/>
    • <b>Mathematical Cause (The Extrapolation Trap):</b> The measured dataset covers the interval $[150, 400]\text{ kB}$. Evaluating at $x = 3\text{ kB}$ represents an extreme extrapolation 147 kB below the data support. Global high-degree polynomials exhibit Runge's phenomenon with violent wild oscillations outside the interpolation interval.
    <br/>
    • <b>Engineering Recommendation:</b> For small packet sizes, engineers should use piecewise linear interpolation or shape-preserving cubic splines (PCHIP) rather than a single high-degree global polynomial.
    """
    story.append(Paragraph(p5_desc, body_style))
    story.append(Spacer(1, 4))

    # Figure 5
    if os.path.exists("figures/fig_problem5.png"):
        story.append(Image("figures/fig_problem5.png", width=420, height=165))
        story.append(Paragraph("<b>Figure 5:</b> Vandermonde polynomial $L(x)$ showing perfect interpolation within $[150, 400]\text{ kB}$ and catastrophic divergence at $x = 3.0\text{ kB}$.", caption_style))
    story.append(Spacer(1, 4))

    # Problem 5 Code & Walkthrough
    story.append(Paragraph("<b>Problem 5 MATLAB Implementation & Code Walkthrough:</b>", h2_style))
    p5_code = load_script("Problem5_Packet_Latency.m")
    for f in make_code_flowables("Problem5_Packet_Latency.m", p5_code, chunk_size=36):
        story.append(f)
        story.append(Spacer(1, 3))
        
    p5_walkthrough = r"""
    <b>Code Walkthrough & Algorithmic Design:</b><br/>
    • <b>Lines 14–25 (Vandermonde Assembly):</b> Uses MATLAB's native <code>vander(x)</code> to construct the $7 \times 7$ power matrix. Computes <code>cond(V)</code> and solves for the coefficient vector <code>c = V \ y</code>.
    <br/>
    • <b>Lines 28–50 (Extrapolation Evaluation):</b> Evaluates the polynomial at $x = 3.0\text{ kB}$ using <code>polyval(c, 3.0)</code>. Formats and prints the condition number, error bound $\text{cond}(V) \cdot \varepsilon$, and the resulting negative latency.
    <br/>
    • <b>Lines 53–75 (Visualization):</b> Generates the dual-panel figure illustrating the localized fit in $[150, 400]\text{ kB}$ alongside the severe downward plunge in $[0, 150]\text{ kB}$.
    """
    story.append(Paragraph(p5_walkthrough, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PROBLEM 6: SATELLITE TO GROUND ENERGY HARVESTING
    # =========================================================================
    story.append(Paragraph("7. Problem 6: Satellite Constellation Wireless Energy Harvesting", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=5))
    
    p6_desc = r"""
    <b>Problem Statement & Research Paper Context:</b><br/>
    Based on Dr. Mohammad Shehab's research paper <i>"Wireless Energy Transfer from Space to Ground via Satellite Constellation Grids"</i> (2024), we analyze a constellation of $N$ Low Earth Orbit (LEO) satellites, each equipped with $M$ antenna elements, wirelessly transferring RF energy to a ground Wirelessly Chargeable Device (WCD). With Maximum Ratio Transmission (MRT), the total harvested energy $E_h$ over access duration $T$ is:
    <br/>
    $$E_h = M N^2 \int_0^T P_h(t)\, dt = M N^2 \mu \int_0^T \frac{dt}{(R+H)^2 + R^2 - 2(R+H)R \cos\phi \cos(\omega t)}$$
    System parameters: Earth radius $R = 6378\text{ km}$, orbital altitude $H = 200\text{ km}$, orbital angular velocity $\omega = 1.182794 \times 10^{-3}\text{ rad/s}$, antennas per satellite $M = 8$, Friis constant $\mu = 8504.072\text{ W}\cdot\text{m}^2$, ground track alignment $\phi = 0$. Access window duration $T = \theta_c / \omega = 2\cos^{-1}(R/(R+H)) / \omega$.
    <br/><br/>
    <b>Part 1: Analytical Closed-Form Derivation (Weierstrass Substitution):</b><br/>
    Defining $A = (R+H)^2 + R^2$ and $B = 2R(R+H)\cos\phi$, we apply the Weierstrass half-angle substitution $u = \tan(\omega t / 2)$, which yields $\cos(\omega t) = \frac{1-u^2}{1+u^2}$ and $dt = \frac{2}{\omega} \frac{du}{1+u^2}$:
    <br/>
    $$E_h = M N^2 \mu \int_0^{\tan(\omega T / 2)} \frac{1}{A - B\left(\frac{1-u^2}{1+u^2}\right)} \left(\frac{2}{\omega (1+u^2)}\right) du = \frac{2 M N^2 \mu}{\omega} \int_0^{\tan(\omega T / 2)} \frac{du}{(A - B) + (A + B)u^2}$$
    For aligned coplanar ground tracks ($\phi = 0$): $A - B = (R+H)^2 + R^2 - 2R(R+H) = H^2$, and $A + B = (R+H)^2 + R^2 + 2R(R+H) = (H + 2R)^2$.
    <br/>
    Therefore: $\sqrt{A^2 - B^2} = \sqrt{(A-B)(A+B)} = H(H + 2R)$, and $\sqrt{\frac{A+B}{A-B}} = \frac{H+2R}{H}$. Integrating:
    <br/>
    $$E_h = \frac{2 M N^2 \mu}{\omega H (H + 2R)} \tan^{-1}\left( \frac{H + 2R}{H} \tan\left(\frac{\omega T}{2}\right) \right)$$
    Applying the complementary arctangent identity $\tan^{-1}(z) = \frac{\pi}{2} - \tan^{-1}(1/z)$:
    <br/>
    $$E_h = \frac{M N^2 \mu}{H^2 \omega + 2 H R \omega} \left[ \pi - 2 \tan^{-1}\left( \frac{H \cot(\omega T / 2)}{H + 2R} \right) \right]$$
    This analytically proves exact equivalence to Dr. Shehab's published formula (2024).
    """
    story.append(Paragraph(p6_desc, body_style))
    story.append(Spacer(1, 4))

    # Harmonized Table 10
    story.append(Paragraph("<b>Part 2 & 3: Numerical Integration & Satellite Scaling ($N = 4:4:32$):</b>", h2_style))
    p6_table_data = [
        [Paragraph("<b>N</b>", table_hdr_style), Paragraph("<b>T [s]</b>", table_hdr_style), Paragraph("<b>Closed-Form [mJ]</b>", table_hdr_style), Paragraph("<b>Trapezoid [mJ]</b>", table_hdr_style), Paragraph("<b>Simpson [mJ]</b>", table_hdr_style), Paragraph("<b>Monte-Carlo [mJ]</b>", table_hdr_style), Paragraph("<b>e<sub>Trap</sub> (%)</b>", table_hdr_style), Paragraph("<b>e<sub>Simp</sub> (%)</b>", table_hdr_style), Paragraph("<b>e<sub>MC</sub> (%)</b>", table_hdr_style)],
        [Paragraph("4", table_cell_center), Paragraph("44.4", table_cell_center), Paragraph("0.7381", table_cell_center), Paragraph("0.7381", table_cell_center), Paragraph("0.7381", table_cell_center), Paragraph("0.7439", table_cell_center), Paragraph("5.21 &times; 10<sup>-4</sup>", table_cell_center), Paragraph("1.50 &times; 10<sup>-8</sup>", table_cell_center), Paragraph("0.78 %", table_cell_center)],
        [Paragraph("8", table_cell_center), Paragraph("99.6", table_cell_center), Paragraph("3.7359", table_cell_center), Paragraph("3.7359", table_cell_center), Paragraph("3.7359", table_cell_center), Paragraph("3.6944", table_cell_center), Paragraph("2.91 &times; 10<sup>-4</sup>", table_cell_center), Paragraph("1.90 &times; 10<sup>-8</sup>", table_cell_center), Paragraph("1.11 %", table_cell_center)],
        [Paragraph("12", table_cell_center), Paragraph("152.4", table_cell_center), Paragraph("8.9604", table_cell_center), Paragraph("8.9604", table_cell_center), Paragraph("8.9604", table_cell_center), Paragraph("8.8949", table_cell_center), Paragraph("1.92 &times; 10<sup>-4</sup>", table_cell_center), Paragraph("1.41 &times; 10<sup>-8</sup>", table_cell_center), Paragraph("0.73 %", table_cell_center)],
        [Paragraph("16", table_cell_center), Paragraph("204.7", table_cell_center), Paragraph("16.4181", table_cell_center), Paragraph("16.4181", table_cell_center), Paragraph("16.4181", table_cell_center), Paragraph("16.5086", table_cell_center), Paragraph("1.42 &times; 10<sup>-4</sup>", table_cell_center), Paragraph("1.09 &times; 10<sup>-8</sup>", table_cell_center), Paragraph("0.55 %", table_cell_center)],
        [Paragraph("20", table_cell_center), Paragraph("257.0", table_cell_center), Paragraph("26.1108", table_cell_center), Paragraph("26.1108", table_cell_center), Paragraph("26.1108", table_cell_center), Paragraph("26.3255", table_cell_center), Paragraph("1.13 &times; 10<sup>-4</sup>", table_cell_center), Paragraph("8.75 &times; 10<sup>-9</sup>", table_cell_center), Paragraph("0.82 %", table_cell_center)],
        [Paragraph("24", table_cell_center), Paragraph("309.5", table_cell_center), Paragraph("38.0400", table_cell_center), Paragraph("38.0399", table_cell_center), Paragraph("38.0400", table_cell_center), Paragraph("37.9426", table_cell_center), Paragraph("9.32 &times; 10<sup>-5</sup>", table_cell_center), Paragraph("7.51 &times; 10<sup>-9</sup>", table_cell_center), Paragraph("0.26 %", table_cell_center)],
        [Paragraph("28", table_cell_center), Paragraph("362.1", table_cell_center), Paragraph("52.2067", table_cell_center), Paragraph("52.2066", table_cell_center), Paragraph("52.2067", table_cell_center), Paragraph("51.6342", table_cell_center), Paragraph("7.93 &times; 10<sup>-5</sup>", table_cell_center), Paragraph("1.64 &times; 10<sup>-8</sup>", table_cell_center), Paragraph("1.10 %", table_cell_center)],
        [Paragraph("32", table_cell_center), Paragraph("415.1", table_cell_center), Paragraph("68.6121", table_cell_center), Paragraph("68.6121", table_cell_center), Paragraph("68.6121", table_cell_center), Paragraph("66.6909", table_cell_center), Paragraph("6.89 &times; 10<sup>-5</sup>", table_cell_center), Paragraph("1.88 &times; 10<sup>-7</sup>", table_cell_center), Paragraph("2.80 %", table_cell_center)],
    ]
    t_p6 = Table(p6_table_data, colWidths=[20, 36, 68, 68, 68, 68, 64, 64, 60])
    t_p6.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_p6)
    story.append(Spacer(1, 4))

    p6_obs = r"""
    • <b>Quadrature Convergence & Error Analysis:</b><br/>
    1. <i>Simpson's 1/3 Rule:</i> Delivers extraordinary accuracy with relative errors between $1.50 \times 10^{-8}\%$ and $1.88 \times 10^{-7}\%$, matching the reference solution to near machine precision.
    <br/>
    2. <i>Multiple Trapezoidal Rule:</i> Demonstrates robust second-order convergence with relative errors between $5.21 \times 10^{-4}\%$ and $6.89 \times 10^{-5}\%$.
    <br/>
    3. <i>Monte-Carlo Integration:</i> Statistical errors fluctuate between $0.26\%$ and $2.80\%$ for $M = 10,000$ random samples, matching the expected $\mathcal{O}(1/\sqrt{M})$ statistical rate.
    <br/>
    4. <i>Constellation Scaling:</i> Harvested energy scales quadratically ($N^2$) from <b>0.74 mJ</b> ($N=4$) to <b>68.61 mJ</b> ($N=32$), demonstrating the massive power gain achieved by coherent beamforming in LEO constellations.
    """
    story.append(Paragraph(p6_obs, body_style))
    story.append(Spacer(1, 4))

    # Figure 6
    if os.path.exists("figures/fig_problem6.png"):
        story.append(Image("figures/fig_problem6.png", width=430, height=165))
        story.append(Paragraph("<b>Figure 6:</b> Harvested energy $E_h$ vs constellation size $N$ (left) and relative true errors on log scale (right) for $K = 100$ and $M = 10,000$ samples.", caption_style))
    story.append(Spacer(1, 4))

    # Problem 6 Code & Walkthrough
    story.append(Paragraph("<b>Problem 6 MATLAB Implementation & Code Walkthrough:</b>", h2_style))
    p6_code = load_script("Problem6_Satellite_Energy_Harvesting.m")
    for f in make_code_flowables("Problem6_Satellite_Energy_Harvesting.m", p6_code, chunk_size=36):
        story.append(f)
        story.append(Spacer(1, 3))
        
    p6_walkthrough = r"""
    <b>Code Walkthrough & Algorithmic Design:</b><br/>
    • <b>Lines 14–48 (Physical Parameters & Analytical Model):</b> Sets orbital constants ($G, M_e, R, H, \omega, \mu$). Defines the analytical closed-form function matching Dr. Shehab's paper.
    <br/>
    • <b>Lines 50–85 (Numerical Quadrature Implementations):</b> Implements the composite trapezoid rule using MATLAB's <code>trapz</code>, composite Simpson's 1/3 rule with alternating $2$ and $4$ weights, and Monte Carlo integration via uniform random sampling <code>rand(M, 1)</code> with a fixed RNG seed (<code>rng(42)</code>) for exact reproducibility.
    <br/>
    • <b>Lines 88–140 (Satellite Sweep Loop):</b> Iterates across $N = 4:4:32$, computing access duration $T$, harvesting integrals, and relative error percentages.
    <br/>
    • <b>Lines 145–190 (Publication Plotting):</b> Creates the dual-axis figure showing quadratic energy scaling on the left and logarithmic error convergence curves on the right.
    """
    story.append(Paragraph(p6_walkthrough, body_style))
    story.append(PageBreak())

    # =========================================================================
    # SECTION 8: MASTER RUNNER & ANTIGRAVITY IDE EXECUTION GUIDE
    # =========================================================================
    story.append(Paragraph("8. Master Automation Script & Antigravity IDE Execution Guide", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=5))
    
    p7_exec = r"""
    <b>Master Automation Script (<code>run_all.m</code>):</b><br/>
    The master script executes all six assignment problems in sequential order, clearing workspace variables between runs, printing execution banners, and rendering all diagnostic figures.
    """
    story.append(Paragraph(p7_exec, body_style))
    story.append(Spacer(1, 4))

    run_all_code = load_script("run_all.m")
    for f in make_code_flowables("run_all.m", run_all_code, chunk_size=36):
        story.append(f)
        story.append(Spacer(1, 3))
    story.append(Spacer(1, 4))

    p7_guide = r"""
    <b>Step-by-Step Instructions to Run Scripts in Antigravity IDE:</b><br/>
    1. <b>Via Integrated Terminal (Fastest Batch Execution):</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;Open the Antigravity IDE terminal (press <code>Ctrl + ~</code>) and enter:
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<code>matlab -batch "cd('MATH502_Assignment1_Submission'); run_all"</code>
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;To run any single problem, replace <code>run_all</code> with <code>Problem1_LORAN</code>, <code>Problem2_RSSI</code>, etc.
    <br/><br/>
    2. <b>Via Interactive MATLAB REPL in Terminal:</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;In PowerShell, start the interactive prompt: <code>matlab -nodesktop -nosplash</code><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;At the <code>&gt;&gt;</code> prompt, navigate and execute: <code>cd MATH502_Assignment1_Submission; run_all</code>
    <br/><br/>
    3. <b>Via Official MathWorks MATLAB Extension:</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;Open any script (e.g. <code>run_all.m</code>). Click the <b>&blacktriangleright; Run</b> icon at the top right of the editor or press <b>F5</b>. Highlight any code section and press <b>Shift + Enter</b> to execute that block.
    """
    story.append(Paragraph(p7_guide, body_style))
    story.append(Spacer(1, 6))

    # Deliverable Box
    deliv_box = r"""
    <b>Submission Verification & Archive Status:</b><br/>
    • All 6 analytical derivations, hand calculations, convergence tables, and figures have been verified.<br/>
    • All MATLAB scripts are fully tested and committed to the official repository: <b>https://github.com/HlozBelloz/MATH502-Numerical-Methods</b>.<br/>
    • The submission package directory <code>MATH502_Assignment1_Submission</code> is complete and ready for submission to <b>bahaaeldin.ibrahim@guc.edu.eg</b>.
    """
    deliv_table = Table([[Paragraph(deliv_box, callout_style)]], colWidths=[516])
    deliv_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdf4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#22c55e')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(deliv_table)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Comprehensive Guide PDF built successfully: {pdf_filename}")
    
    # Copy to root directory
    root_pdf = "MATH502_Assignment1_Solutions_and_Code_Guide.pdf"
    shutil.copyfile(pdf_filename, root_pdf)
    print(f"Copied to root workspace: {root_pdf}")

if __name__ == '__main__':
    build_pdf()

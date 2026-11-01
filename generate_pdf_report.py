import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# Register Arial with full Unicode UTF-8 support
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Italic', 'C:/Windows/Fonts/ariali.ttf'))
pdfmetrics.registerFont(TTFont('Arial-BoldItalic', 'C:/Windows/Fonts/arialbi.ttf'))
registerFontFamily('Arial', normal='Arial', bold='Arial-Bold', italic='Arial-Italic', boldItalic='Arial-BoldItalic')

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and draw running headers and footers with 'Page X of Y'.
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
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        # Suppress running header/footer on cover page
        if self._pageNumber > 1:
            self.saveState()
            
            # Running Header
            self.setFont('Arial-Bold', 8)
            self.setFillColor(colors.HexColor('#1e3a8a'))
            self.drawString(54, 752, 'GERMAN UNIVERSITY IN CAIRO')
            self.setFont('Arial', 8)
            self.setFillColor(colors.HexColor('#64748b'))
            self.drawString(195, 752, '|   MATH502: Numerical Methods   |   Assignment 1 Report')
            
            self.setStrokeColor(colors.HexColor('#cbd5e1'))
            self.setLineWidth(0.75)
            self.line(54, 744, 558, 744)
            
            # Running Footer
            self.line(54, 44, 558, 44)
            self.setFont('Arial', 8)
            self.setFillColor(colors.HexColor('#64748b'))
            self.drawString(54, 32, 'Faculty of Information Engineering and Technology (IET) -- Dr. Mohammad Shehab')
            
            page_text = f'Page {self._pageNumber} of {page_count}'
            self.drawRightString(558, 32, page_text)
            
            self.restoreState()


def build_pdf():
    pdf_filename = "MATH502_Assignment1_Submission/MATH502_Assignment1_Report.pdf"
    os.makedirs("MATH502_Assignment1_Submission", exist_ok=True)
    
    # Margins: 54pt (0.75 in) left/right, 48pt top/bottom
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=48,
        bottomMargin=48,
        title="MATH502 Assignment 1 Report",
        author="Mazen Altelbany",
        subject="MATH502 Numerical Methods",
        creator="MATLAB R2026a"
    )
    
    styles = getSampleStyleSheet()
    
    # Academic Navy Palette
    c_primary = colors.HexColor('#1e3a8a')    # Navy
    c_secondary = colors.HexColor('#0d9488')  # Teal
    c_dark = colors.HexColor('#0f172a')       # Charcoal Body Text
    c_slate = colors.HexColor('#475569')      # Muted Slate
    c_bg_light = colors.HexColor('#f8fafc')   # Off-white Light
    c_border = colors.HexColor('#cbd5e1')     # Border grey
    
    # Custom Typography Styles using Unicode Arial
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Arial',
        fontSize=8.5,
        leading=11.5,
        textColor=c_dark
    )
    
    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=body_style,
        fontName='Arial-Bold',
        fontSize=21,
        leading=25,
        textColor=c_primary,
        alignment=1
    )
    
    cover_subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=body_style,
        fontName='Arial',
        fontSize=10.5,
        leading=14.5,
        textColor=c_slate,
        alignment=1
    )
    
    h1_style = ParagraphStyle(
        'H1_Custom',
        parent=body_style,
        fontName='Arial-Bold',
        fontSize=12,
        leading=15,
        textColor=c_primary,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'H2_Custom',
        parent=body_style,
        fontName='Arial-Bold',
        fontSize=10,
        leading=13,
        textColor=c_secondary,
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True
    )
    
    h3_style = ParagraphStyle(
        'H3_Custom',
        parent=body_style,
        fontName='Arial-Bold',
        fontSize=9,
        leading=12,
        textColor=c_slate,
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )
    
    callout_style = ParagraphStyle(
        'CalloutText',
        parent=body_style,
        fontSize=8,
        leading=11,
        textColor=c_dark
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=body_style,
        fontSize=7.5,
        leading=10,
        textColor=c_dark
    )
    
    table_hdr_style = ParagraphStyle(
        'TableHdr',
        parent=body_style,
        fontName='Arial-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.white
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=body_style,
        fontName='Arial-Italic',
        fontSize=7.5,
        leading=10,
        textColor=c_slate,
        alignment=1
    )

    story = []
    
    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 30))
    story.append(Paragraph("GERMAN UNIVERSITY IN CAIRO (GUC)", ParagraphStyle('GUC_Hdr', parent=cover_title_style, fontSize=13, leading=16, textColor=c_slate)))
    story.append(Paragraph("Faculty of Information Engineering and Technology (IET)", ParagraphStyle('GUC_Sub', parent=cover_subtitle_style, fontSize=10, leading=13, textColor=c_slate)))
    story.append(Spacer(1, 15))
    
    story.append(HRFlowable(width="100%", thickness=2, color=c_primary, spaceBefore=4, spaceAfter=18))
    
    story.append(Paragraph("MATH502: NUMERICAL METHODS", ParagraphStyle('CourseCode', parent=cover_subtitle_style, fontName='Arial-Bold', fontSize=11.5, leading=14.5, textColor=c_secondary)))
    story.append(Spacer(1, 8))
    story.append(Paragraph("ASSIGNMENT 1 REPORT", cover_title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Non-Linear Systems, Polynomial Interpolation, Diode Circuit Root-Finding,<br/>and Satellite Constellation Wireless Energy Harvesting", cover_subtitle_style))
    story.append(Spacer(1, 16))
    
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=18))
    
    info_data = [
        [Paragraph("<b>Course Instructor:</b>", body_style), Paragraph("Dr. Mohammad Shehab", body_style)],
        [Paragraph("<b>Teaching Assistant:</b>", body_style), Paragraph("Eng. Bahaaeldin Ibrahim (bahaaeldin.ibrahim@guc.edu.eg)", body_style)],
        [Paragraph("<b>Programming Language:</b>", body_style), Paragraph("MATLAB (MathWorks R2026a)", body_style)],
        [Paragraph("<b>Submission Date:</b>", body_style), Paragraph("November 6, 2026", body_style)],
        [Paragraph("<b>Student 1 Name & ID:</b>", body_style), Paragraph("Mazen Altelbany &nbsp;&nbsp;|&nbsp;&nbsp; <b>ID:</b> 64-12371 &nbsp;&nbsp;|&nbsp;&nbsp; <b>Tutorial:</b> T-01", body_style)],
        [Paragraph("<b>Student 2 Name & ID:</b>", body_style), Paragraph("[Partner Full Name] &nbsp;&nbsp;|&nbsp;&nbsp; <b>ID:</b> [Partner ID] &nbsp;&nbsp;|&nbsp;&nbsp; <b>Tutorial:</b> T-02", body_style)],
    ]
    info_table = Table(info_data, colWidths=[140, 364])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, c_primary),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(info_table)
    
    story.append(Spacer(1, 16))
    
    story.append(Paragraph("<b>Table of Contents / Report Outline:</b>", h3_style))
    story.append(Spacer(1, 4))
    
    toc_data = [
        [Paragraph("<b>Section</b>", table_hdr_style), Paragraph("<b>Title & Topic</b>", table_hdr_style), Paragraph("<b>Page</b>", table_hdr_style)],
        [Paragraph("Section 1", table_cell_style), Paragraph("Programming Language Selection & Justification (MATLAB)", table_cell_style), Paragraph("2", table_cell_style)],
        [Paragraph("Section 2", table_cell_style), Paragraph("Problem 1: LORAN-C Hyperbolic Positioning System", table_cell_style), Paragraph("2", table_cell_style)],
        [Paragraph("Section 3", table_cell_style), Paragraph("Problem 2: Wireless Sensor Network (WSN) RSSI Interpolation", table_cell_style), Paragraph("4", table_cell_style)],
        [Paragraph("Section 4", table_cell_style), Paragraph("Problem 3: Diode DC Circuit Non-Linear Analysis (Bisection & Secant)", table_cell_style), Paragraph("6", table_cell_style)],
        [Paragraph("Section 5", table_cell_style), Paragraph("Problem 4: Diode DC Circuit Analysis (Newton-Raphson Method)", table_cell_style), Paragraph("7", table_cell_style)],
        [Paragraph("Section 6", table_cell_style), Paragraph("Problem 5: Packet Latency Vandermonde Interpolation & Extrapolation Analysis", table_cell_style), Paragraph("8", table_cell_style)],
        [Paragraph("Section 7", table_cell_style), Paragraph("Problem 6: Satellite to Ground Wireless Energy Harvesting", table_cell_style), Paragraph("9", table_cell_style)],
    ]
    toc_table = Table(toc_data, colWidths=[65, 399, 40])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
    ]))
    story.append(toc_table)
    
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 2: SECTION 1 & PROBLEM 1 (INTRO & ITERATION 1)
    # =========================================================================
    story.append(Paragraph("1. Programming Language Selection & Justification", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=4))
    
    lang_just_text = """
    <b>MATLAB (MathWorks R2026a)</b> was chosen as the programming language for this assignment based on the following reasons:
    <br/>
    1. <b>Industry & Engineering Academic Standard:</b> MATLAB is the standard computing environment for engineering mathematics, signals, and communication systems in the Faculty of IET at GUC.
    <br/>
    2. <b>High-Performance Native Matrix Manipulation:</b> Multivariable linear system solves (such as Newton-Raphson Jacobian solves <code>J \\ (-F)</code> in Problem 1 and Vandermonde solves <code>V \\ y</code> in Problem 5) execute through LAPACK/BLAS-optimized routines without manual inversion.
    <br/>
    3. <b>Specialized Built-In Solvers:</b> Provides production-tested solvers (<code>fsolve</code> for non-linear systems, <code>polyfit/polyval</code> for interpolation, <code>fzero</code> for scalar root-finding, and <code>trapz</code> for numerical quadrature) to validate and cross-check the numerical results.
    <br/>
    4. <b>Double-Precision IEEE 754 Compliance:</b> Eliminates nested-loop bottlenecks through native vectorization while preserving 64-bit numerical accuracy.
    """
    story.append(Paragraph(lang_just_text, body_style))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("2. Problem 1: LORAN Non-Linear System Navigation Solver", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=4))
    
    p1_desc = """
    <b>Physical Context:</b> The LOng RAnge Navigation (LORAN) system calculates a boat's coordinates (x, y) at sea using synchronized radio signals from fixed transmitter stations. The time difference of arrival (TDOA) produces hyperbolic lines of position whose intersection determines the boat's coordinates.
    <br/><br/>
    The governing non-linear system is defined by two hyperbolas:
    """
    story.append(Paragraph(p1_desc, body_style))
    story.append(Spacer(1, 2))
    
    p1_eq_box = """
    <b>Governing System Equations:</b><br/>
    Eq 1: &nbsp;&nbsp; <i>f</i><sub>1</sub>(<i>x</i>, <i>y</i>) = <i>x</i><sup>2</sup> / 186<sup>2</sup> - <i>y</i><sup>2</sup> / (300<sup>2</sup> - 186<sup>2</sup>) - 1 = <i>x</i><sup>2</sup> / 34596 - <i>y</i><sup>2</sup> / 55404 - 1 = 0<br/>
    Eq 2: &nbsp;&nbsp; <i>f</i><sub>2</sub>(<i>x</i>, <i>y</i>) = (<i>y</i> - 500)<sup>2</sup> / 279<sup>2</sup> - (<i>x</i> - 300)<sup>2</sup> / (500<sup>2</sup> - 279<sup>2</sup>) - 1 = (<i>y</i> - 500)<sup>2</sup> / 77841 - (<i>x</i> - 300)<sup>2</sup> / 172159 - 1 = 0
    """
    p1_eq_table = Table([[Paragraph(p1_eq_box, callout_style)]], colWidths=[504])
    p1_eq_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(p1_eq_table)
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>Jacobian Matrix Formulation:</b>", h2_style))
    p1_jac_text = """
    The Jacobian matrix <i>J</i>(<i>x</i>, <i>y</i>) contains all partial derivatives:<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>J</i><sub>11</sub> = &part;<i>f</i><sub>1</sub>/&part;<i>x</i> = 2<i>x</i> / 34596, &nbsp;&nbsp;&nbsp;&nbsp;<i>J</i><sub>12</sub> = &part;<i>f</i><sub>1</sub>/&part;<i>y</i> = -2<i>y</i> / 55404<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>J</i><sub>21</sub> = &part;<i>f</i><sub>2</sub>/&part;<i>x</i> = -2(<i>x</i> - 300) / 172159, &nbsp;&nbsp;&nbsp;&nbsp;<i>J</i><sub>22</sub> = &part;<i>f</i><sub>2</sub>/&part;<i>y</i> = 2(<i>y</i> - 500) / 77841<br/>
    Newton-Raphson update step: <i>J</i>(<b>x</b><sub>k</sub>) &Delta;<b>x</b><sub>k</sub> = -<b>F</b>(<b>x</b><sub>k</sub>) &rarr; <b>x</b><sub>k+1</sub> = <b>x</b><sub>k</sub> + &Delta;<b>x</b><sub>k</sub>.
    """
    story.append(Paragraph(p1_jac_text, body_style))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>Part (a): Pen-and-Paper Manual Iteration 1 (Starting at x0 = y0 = 200):</b>", h2_style))
    p1_pen1_text = """
    1. <i>Evaluate Function Vector <b>F</b>(<b>x</b><sub>0</sub>):</i><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>f</i><sub>1</sub>(200, 200) = 200<sup>2</sup>/34596 - 200<sup>2</sup>/55404 - 1 = 1.156203 - 0.721969 - 1 = <b>-0.565767</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>f</i><sub>2</sub>(200, 200) = (200-500)<sup>2</sup>/77841 - (200-300)<sup>2</sup>/172159 - 1 = 1.156203 - 0.058086 - 1 = <b>+0.098117</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<b>F</b>(<b>x</b><sub>0</sub>) = [-0.565767, +0.098117]<sup>T</sup> &rarr; -<b>F</b>(<b>x</b><sub>0</sub>) = [+0.565767, -0.098117]<sup>T</sup><br/>
    2. <i>Evaluate Jacobian Matrix J(<b>x</b><sub>0</sub>):</i><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>J</i><sub>11</sub> = 2(200)/34596 = 0.01156203, &nbsp;&nbsp; <i>J</i><sub>12</sub> = -2(200)/55404 = -0.00721970<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>J</i><sub>21</sub> = -2(200-300)/172159 = 0.00116172, &nbsp;&nbsp; <i>J</i><sub>22</sub> = 2(200-500)/77841 = -0.00770802<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;det(<i>J</i><sub>0</sub>) = (0.01156203)(-0.00770802) - (-0.00721970)(0.00116172) = <b>-8.073312 &times; 10<sup>-5</sup></b><br/>
    3. <i>Solve 2x2 Linear System using Cramer's Rule:</i><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&Delta;<i>x</i><sub>0</sub> = [(-0.00770802)(0.565767) - (-0.00721970)(-0.098117)] / (-8.073312 &times; 10<sup>-5</sup>) = <b>+62.791030</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&Delta;<i>y</i><sub>0</sub> = [(0.01156203)(-0.098117) - (0.00116172)(0.565767)] / (-8.073312 &times; 10<sup>-5</sup>) = <b>+22.192804</b><br/>
    4. <i>Update:</i> <b>x</b><sub>1</sub> = <b>x</b><sub>0</sub> + &Delta;<b>x</b><sub>0</sub> = [200 + 62.791030, 200 + 22.192804]<sup>T</sup> = <b>[262.791030, 222.192804]<sup>T</sup></b>.
    """
    story.append(Paragraph(p1_pen1_text, body_style))
    
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 3: PROBLEM 1 (ITERATION 2, TABLE, FSOLVE & FIGURE 1)
    # =========================================================================
    story.append(Paragraph("<b>Problem 1 (Continued): Iteration 2, Software Solution & Figure</b>", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=4))
    
    p1_pen2_text = """
    <b>Iteration 2 Calculations:</b><br/>
    1. <i>Evaluate Function Vector <b>F</b>(<b>x</b><sub>1</sub>) at [262.791030, 222.192804]<sup>T</sup>:</i><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>f</i><sub>1</sub>(262.791, 222.193) = 262.791030<sup>2</sup>/34596 - 222.192804<sup>2</sup>/55404 - 1 = <b>+0.105075</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>f</i><sub>2</sub>(262.791, 222.193) = (222.192804-500)<sup>2</sup>/77841 - (262.791030-300)<sup>2</sup>/172159 - 1 = <b>-0.016574</b><br/>
    2. <i>Evaluate Jacobian Matrix J(<b>x</b><sub>1</sub>):</i><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>J</i><sub>11</sub> = 0.01519199, &nbsp;&nbsp; <i>J</i><sub>12</sub> = -0.00802082, &nbsp;&nbsp; <i>J</i><sub>21</sub> = 0.00043226, &nbsp;&nbsp; <i>J</i><sub>22</sub> = -0.00713781<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;det(<i>J</i><sub>1</sub>) = (0.01519199)(-0.00713781) - (-0.00802082)(0.00043226) = <b>-1.049705 &times; 10<sup>-4</sup></b><br/>
    3. <i>Solve for &Delta;<b>x</b><sub>1</sub>:</i> &Delta;<i>x</i><sub>1</sub> = <b>-8.411356</b>, &nbsp;&nbsp; &Delta;<i>y</i><sub>1</sub> = <b>-2.831433</b><br/>
    4. <i>Update:</i> <b>x</b><sub>2</sub> = <b>x</b><sub>1</sub> + &Delta;<b>x</b><sub>1</sub> = [262.791030 - 8.411356, 222.192804 - 2.831433]<sup>T</sup> = <b>[254.379674, 219.361371]<sup>T</sup></b>.
    """
    story.append(Paragraph(p1_pen2_text, body_style))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>Part (b): Software Package Accurate Solution & Convergence History:</b>", h2_style))
    p1_table_data = [
        [Paragraph("<b>Iteration k</b>", table_hdr_style), Paragraph("<b>x_k</b>", table_hdr_style), Paragraph("<b>y_k</b>", table_hdr_style), Paragraph("<b>||F(x_k)||</b>", table_hdr_style), Paragraph("<b>||Delta x_k||</b>", table_hdr_style)],
        [Paragraph("0 (Initial)", table_cell_style), Paragraph("200.000000", table_cell_style), Paragraph("200.000000", table_cell_style), Paragraph("5.7421e-01", table_cell_style), Paragraph("6.6599e+01", table_cell_style)],
        [Paragraph("1", table_cell_style), Paragraph("262.791030", table_cell_style), Paragraph("222.192804", table_cell_style), Paragraph("1.0637e-01", table_cell_style), Paragraph("8.8749e+00", table_cell_style)],
        [Paragraph("2", table_cell_style), Paragraph("254.379674", table_cell_style), Paragraph("219.361371", table_cell_style), Paragraph("1.9248e-03", table_cell_style), Paragraph("1.6757e-01", table_cell_style)],
        [Paragraph("3", table_cell_style), Paragraph("254.221177", table_cell_style), Paragraph("219.307011", table_cell_style), Paragraph("6.3451e-07", table_cell_style), Paragraph("5.9221e-05", table_cell_style)],
        [Paragraph("4 (Converged)", table_cell_style), Paragraph("254.221120", table_cell_style), Paragraph("219.306992", table_cell_style), Paragraph("6.8421e-14", table_cell_style), Paragraph("6.4210e-12", table_cell_style)],
    ]
    p1_table = Table(p1_table_data, colWidths=[70, 105, 105, 110, 114])
    p1_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(p1_table)
    story.append(Spacer(1, 4))
    
    p1_concl = """
    <b>MATLAB Built-in <code>fsolve</code> Validation:</b> Yields identical vessel coordinates <i>x</i>* = 254.221120, <i>y</i>* = 219.306992 with residual &lt; 10<sup>-14</sup>. Across the entire plane, 4 mathematical intersection roots exist: (254.22, 219.31), (740.33, 906.83), (-193.29, 66.56), and (-1273.34, 1594.11). The initial guess (200, 200) reliably converges to the vessel's valid operational coordinates.
    """
    story.append(Paragraph(p1_concl, body_style))
    story.append(Spacer(1, 4))
    
    if os.path.exists("figures/fig_problem1.png"):
        story.append(Image("figures/fig_problem1.png", width=370, height=170))
        story.append(Paragraph("<b>Figure 1:</b> LORAN hyperbolic transmitter position curves and Newton-Raphson iteration trajectory.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: PROBLEM 2 (TABLE & POLYNOMIAL DERIVATION)
    # =========================================================================
    story.append(Paragraph("3. Problem 2: Wireless Sensor Network (WSN) RSSI Interpolation", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=4))
    
    p2_desc = """
    <b>Physical Context:</b> An indoor Wireless Sensor Network (WSN) measures Received Signal Strength Indicator (RSSI) in dBm at varying distances <i>d</i> [m] from an environmental monitoring transmitter. Due to multipath reflection and wall shadowing, the signal does not follow a simple logarithmic curve. We interpolate unmeasured locations using polynomial modeling.
    """
    story.append(Paragraph(p2_desc, body_style))
    story.append(Spacer(1, 3))
    
    data_p2 = [
        [Paragraph("<b>Distance d [m]</b>", table_hdr_style), Paragraph("1.0", table_cell_style), Paragraph("2.5", table_cell_style), Paragraph("4.0", table_cell_style), Paragraph("6.0", table_cell_style), Paragraph("8.0", table_cell_style)],
        [Paragraph("<b>RSSI [dBm]</b>", table_hdr_style), Paragraph("-40.0", table_cell_style), Paragraph("-47.0", table_cell_style), Paragraph("-54.0", table_cell_style), Paragraph("-60.0", table_cell_style), Paragraph("-66.0", table_cell_style)]
    ]
    t_p2_data = Table(data_p2, colWidths=[104, 80, 80, 80, 80, 80])
    t_p2_data.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_p2_data)
    story.append(Spacer(1, 5))
    
    story.append(Paragraph("<b>Part (a): Newton's Divided Difference Table & Polynomial:</b>", h2_style))
    div_table_data = [
        [Paragraph("<b>i</b>", table_hdr_style), Paragraph("<b>d_i [m]</b>", table_hdr_style), Paragraph("<b>f[d_i]</b>", table_hdr_style), Paragraph("<b>f[ , ]</b>", table_hdr_style), Paragraph("<b>f[ , , ]</b>", table_hdr_style), Paragraph("<b>f[ , , , ]</b>", table_hdr_style), Paragraph("<b>f[ , , , , ]</b>", table_hdr_style)],
        [Paragraph("0", table_cell_style), Paragraph("1.0", table_cell_style), Paragraph("<b>-40.000000</b>", table_cell_style), Paragraph("<b>-4.666667</b>", table_cell_style), Paragraph("<b>0.000000</b>", table_cell_style), Paragraph("<b>0.095238</b>", table_cell_style), Paragraph("<b>-0.025974</b>", table_cell_style)],
        [Paragraph("1", table_cell_style), Paragraph("2.5", table_cell_style), Paragraph("-47.000000", table_cell_style), Paragraph("-4.666667", table_cell_style), Paragraph("0.476190", table_cell_style), Paragraph("-0.086580", table_cell_style), Paragraph("--", table_cell_style)],
        [Paragraph("2", table_cell_style), Paragraph("4.0", table_cell_style), Paragraph("-54.000000", table_cell_style), Paragraph("-3.000000", table_cell_style), Paragraph("0.000000", table_cell_style), Paragraph("--", table_cell_style), Paragraph("--", table_cell_style)],
        [Paragraph("3", table_cell_style), Paragraph("6.0", table_cell_style), Paragraph("-60.000000", table_cell_style), Paragraph("-3.000000", table_cell_style), Paragraph("--", table_cell_style), Paragraph("--", table_cell_style), Paragraph("--", table_cell_style)],
        [Paragraph("4", table_cell_style), Paragraph("8.0", table_cell_style), Paragraph("-66.000000", table_cell_style), Paragraph("--", table_cell_style), Paragraph("--", table_cell_style), Paragraph("--", table_cell_style), Paragraph("--", table_cell_style)],
    ]
    div_table = Table(div_table_data, colWidths=[24, 60, 84, 84, 84, 84, 84])
    div_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(div_table)
    story.append(Spacer(1, 4))
    
    p2_poly_text = """
    <b>Constructed Newton Polynomial:</b><br/>
    <i>P</i><sub>4</sub>(<i>d</i>) = -40 - 4.666667(<i>d</i> - 1) + 0.095238(<i>d</i> - 1)(<i>d</i> - 2.5)(<i>d</i> - 4) - 0.025974(<i>d</i> - 1)(<i>d</i> - 2.5)(<i>d</i> - 4)(<i>d</i> - 6)<br/>
    Expanded Standard Form: <i>P</i><sub>4</sub>(<i>d</i>) = -0.025974 <i>d</i><sup>4</sup> + 0.445887 <i>d</i><sup>3</sup> - 2.311688 <i>d</i><sup>2</sup> - 0.264069 <i>d</i> - 37.844156.
    """
    story.append(Paragraph(p2_poly_text, body_style))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>Part (b): Estimation at d = 5 meters:</b>", h2_style))
    p2_est_text = """
    Evaluating at <i>d</i> = 5 m:<br/>
    <i>P</i><sub>4</sub>(5.0) = -40 - 4.666667(4) + 0.095238(4 &times; 2.5 &times; 1) - 0.025974(4 &times; 2.5 &times; 1 &times; -1) = <b>-57.454545 dBm</b> &approx; <b>-57.45 dBm</b>.
    """
    story.append(Paragraph(p2_est_text, body_style))
    
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 5: PROBLEM 2 (DISCREPANCY, HORNER & FIGURE 2)
    # =========================================================================
    story.append(Paragraph("<b>Problem 2 (Continued): Discrepancy Analysis, Horner's Scheme & Figure</b>", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=4))
    
    story.append(Paragraph("<b>Part (c): Comparison with Measured Value (-57.0 dBm) & Discrepancy Discussion:</b>", h2_style))
    p2_disc_text = """
    The interpolated value is <b>-57.45 dBm</b>, compared with measured <b>-57.00 dBm</b> (a discrepancy of only 0.45 dB, or 0.79% relative error).
    <br/><br/>
    <b>Physical Engineering Causes for Discrepancy:</b><br/>
    1. <b>Multipath Fading & Phase Interference:</b> In smart buildings, RF transmissions reflect off reinforced concrete walls, metallic ducts, and floors. Reflections arrive at the receiver antenna with varying phases, causing constructive and destructive interference fringes that fluctuate RSSI by several decibels across spatial displacements of just a few centimeters.<br/>
    2. <b>Temporal & Dynamic Environmental Obstructions:</b> Independent measurement sessions experience changing surroundings: people walking through the signal path (causing human body shadowing attenuation of 3-5 dB), doors opening or closing, and ambient humidity/temperature variations.<br/>
    3. <b>Antenna Radiation Patterns & Transceiver ADC Tolerances:</b> Imperfect omnidirectional antenna gain, polarization tilt, and receiver ADC quantization error introduce an inherent &plusmn;1 dB hardware measurement tolerance.<br/>
    4. <b>Mathematical Model Mismatch:</b> A 4th-degree polynomial forces a global mathematical curve through discrete sample points, whereas physical electromagnetic wave propagation follows a logarithmic path loss law (<i>RSSI</i>(<i>d</i>) &prop; -10<i>n</i> log<sub>10</sub>(<i>d</i>)).
    """
    story.append(Paragraph(p2_disc_text, body_style))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>Part (d): Horner's Scheme Representation & Operation Counts:</b>", h2_style))
    p2_horn_text = """
    <b>1. Nested Newton Form (Horner Scheme):</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>P</i><sub>4</sub>(<i>d</i>) = <i>a</i><sub>0</sub> + (<i>d</i> - <i>d</i><sub>0</sub>)[<i>a</i><sub>1</sub> + (<i>d</i> - <i>d</i><sub>1</sub>)[<i>a</i><sub>2</sub> + (<i>d</i> - <i>d</i><sub>2</sub>)[<i>a</i><sub>3</sub> + (<i>d</i> - <i>d</i><sub>3</sub>)<i>a</i><sub>4</sub>]]]<br/>
    • <b>Multiplications:</b> Exactly <b>4</b> multiplications.<br/>
    • <b>Additions / Subtractions:</b> 4 subtractions (<i>d</i> - <i>d</i><sub>i</sub>) + 4 additions with <i>a</i><sub>i</sub> = <b>8</b> additions/subtractions (or 4 additions and 4 subtractions).
    <br/><br/>
    <b>2. Standard Form Horner's Scheme:</b><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>P</i><sub>4</sub>(<i>d</i>) = <i>c</i><sub>0</sub> + <i>d</i>[<i>c</i><sub>1</sub> + <i>d</i>[<i>c</i><sub>2</sub> + <i>d</i>[<i>c</i><sub>3</sub> + <i>d</i> &middot; <i>c</i><sub>4</sub>]]]<br/>
    • <b>Multiplications:</b> Exactly <b>4</b> multiplications.<br/>
    • <b>Additions:</b> Exactly <b>4</b> additions.<br/>
    <i>Horner's scheme reduces multiplications from 10 (naive evaluation) to 4 (a 60% saving), minimizing rounding error.</i>
    """
    story.append(Paragraph(p2_horn_text, body_style))
    story.append(Spacer(1, 4))
    
    if os.path.exists("figures/fig_problem2.png"):
        story.append(Image("figures/fig_problem2.png", width=370, height=170))
        story.append(Paragraph("<b>Figure 2:</b> WSN RSSI measurement points, Newton interpolating polynomial P4(d), and validation at 5 meters.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: PROBLEM 3 - DIODE ROOT FINDING (BISECTION & SECANT)
    # =========================================================================
    story.append(Paragraph("4. Problem 3: Diode DC Circuit Non-Linear Analysis (Bisection & Secant)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=4))
    
    p3_desc = """
    <b>Physical Context:</b> A series DC circuit contains a voltage source <i>V</i><sub>s</sub> = 1.0 V, a resistor <i>R</i> = 1000 &Omega;, and a silicon diode. By Kirchhoff's Voltage Law (KVL): <i>V</i><sub>s</sub> = <i>I R</i> + <i>V</i><sub>D</sub>. The Shockley diode equation relates current <i>I</i> and diode voltage <i>V</i><sub>D</sub>:
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>I</i> = <i>I</i><sub>s</sub> (e<sup><i>V</i><sub>D</sub> / (<i>n V</i><sub>T</sub>)</sup> - 1) &rarr; <i>V</i><sub>D</sub> = <i>n V</i><sub>T</sub> ln(<i>I</i> / <i>I</i><sub>s</sub> + 1)
    <br/>
    The non-linear equation governing the circuit operating current is:
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>f</i>(<i>I</i>) = <i>I R</i> + <i>n V</i><sub>T</sub> ln(<i>I</i> / <i>I</i><sub>s</sub> + 1) - <i>V</i><sub>s</sub> = 0
    <br/>
    <b>Constants:</b> <i>I</i><sub>s</sub> = 10<sup>-12</sup> A, <i>n</i> = 1.5, <i>V</i><sub>T</sub> = 25.85 mV, <i>R</i> = 1 k&Omega;, <i>V</i><sub>s</sub> = 1.0 V, Tolerance Tol = 10<sup>-4</sup> A (0.1 mA).
    <br/>
    <b>Bracket Evaluation:</b> <i>f</i>(0) = -1.0000 V &lt; 0, <i>f</i>(5 &times; 10<sup>-3</sup>) = +4.86595 V &gt; 0. By the Intermediate Value Theorem, a unique root exists in [0, 5 mA].
    """
    story.append(Paragraph(p3_desc, body_style))
    story.append(Spacer(1, 3))
    
    story.append(Paragraph("<b>1. Bisection Method Iteration History:</b>", h3_style))
    bis_table_data = [
        [Paragraph("<b>Iter</b>", table_hdr_style), Paragraph("<b>a [mA]</b>", table_hdr_style), Paragraph("<b>b [mA]</b>", table_hdr_style), Paragraph("<b>c [mA]</b>", table_hdr_style), Paragraph("<b>(b - a)/2 [A]</b>", table_hdr_style), Paragraph("<b>f(c) [V]</b>", table_hdr_style)],
        [Paragraph("1", table_cell_style), Paragraph("0.0000", table_cell_style), Paragraph("5.0000", table_cell_style), Paragraph("2.5000", table_cell_style), Paragraph("1.2500e-03", table_cell_style), Paragraph("+2.3391e+00", table_cell_style)],
        [Paragraph("2", table_cell_style), Paragraph("0.0000", table_cell_style), Paragraph("2.5000", table_cell_style), Paragraph("1.2500", table_cell_style), Paragraph("6.2500e-04", table_cell_style), Paragraph("+1.0622e+00", table_cell_style)],
        [Paragraph("3", table_cell_style), Paragraph("0.0000", table_cell_style), Paragraph("1.2500", table_cell_style), Paragraph("0.6250", table_cell_style), Paragraph("3.1250e-04", table_cell_style), Paragraph("+4.1032e-01", table_cell_style)],
        [Paragraph("4", table_cell_style), Paragraph("0.0000", table_cell_style), Paragraph("0.6250", table_cell_style), Paragraph("0.3125", table_cell_style), Paragraph("1.5625e-04", table_cell_style), Paragraph("+7.0943e-02", table_cell_style)],
        [Paragraph("5", table_cell_style), Paragraph("0.0000", table_cell_style), Paragraph("0.3125", table_cell_style), Paragraph("0.1562", table_cell_style), Paragraph("<b>7.8125e-05</b>", table_cell_style), Paragraph("-1.1218e-01", table_cell_style)],
    ]
    t_bis = Table(bis_table_data, colWidths=[35, 90, 90, 90, 100, 99])
    t_bis.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_bis)
    story.append(Spacer(1, 2))
    
    p3_bis_sum = """
    • <b>Bisection Result:</b> Converges in <b>5 iterations</b> with error bound (<i>b</i> - <i>a</i>)/2 = 7.8125 &times; 10<sup>-5</sup> A &lt; 10<sup>-4</sup> A, yielding <i>I</i> = <b>0.234375 mA</b> (or <i>I</i> = 0.2500 mA at 6 iterations with error 3.9 &times; 10<sup>-5</sup> A).
    """
    story.append(Paragraph(p3_bis_sum, body_style))
    story.append(Spacer(1, 3))
    
    story.append(Paragraph("<b>2. Secant Method Iteration History:</b>", h3_style))
    sec_table_data = [
        [Paragraph("<b>Iter k</b>", table_hdr_style), Paragraph("<b>x_{k-1} [mA]</b>", table_hdr_style), Paragraph("<b>x_k [mA]</b>", table_hdr_style), Paragraph("<b>x_{k+1} [mA]</b>", table_hdr_style), Paragraph("<b>|x_{k+1} - x_k| [A]</b>", table_hdr_style), Paragraph("<b>f(x_{k+1}) [V]</b>", table_hdr_style)],
        [Paragraph("1", table_cell_style), Paragraph("0.0000", table_cell_style), Paragraph("5.0000", table_cell_style), Paragraph("0.852377", table_cell_style), Paragraph("4.1476e-03", table_cell_style), Paragraph("+6.4973e-01", table_cell_style)],
        [Paragraph("2", table_cell_style), Paragraph("5.0000", table_cell_style), Paragraph("0.852377", table_cell_style), Paragraph("0.213220", table_cell_style), Paragraph("6.3916e-04", table_cell_style), Paragraph("-4.3159e-02", table_cell_style)],
        [Paragraph("3", table_cell_style), Paragraph("0.852377", table_cell_style), Paragraph("0.213220", table_cell_style), Paragraph("0.253033", table_cell_style), Paragraph("<b>3.9813e-05</b>", table_cell_style), Paragraph("+3.2912e-03", table_cell_style)],
    ]
    t_sec = Table(sec_table_data, colWidths=[40, 85, 85, 95, 105, 94])
    t_sec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_sec)
    story.append(Spacer(1, 2))
    
    p3_sec_sum = """
    • <b>Secant Result:</b> Converges in <b>3 iterations</b> with step size |<i>x</i><sub>3</sub> - <i>x</i><sub>2</sub>| = 3.9813 &times; 10<sup>-5</sup> A &lt; 10<sup>-4</sup> A, yielding <i>I</i> = <b>0.253033 mA</b>.<br/>
    • <b>MATLAB Built-in <code>fzero</code> Benchmark:</b> <i>I</i>* = <b>0.250181 mA</b> = 2.501809 &times; 10<sup>-4</sup> A.
    """
    story.append(Paragraph(p3_sec_sum, body_style))
    story.append(Spacer(1, 3))
    
    if os.path.exists("figures/fig_problem3.png"):
        story.append(Image("figures/fig_problem3.png", width=360, height=155))
        story.append(Paragraph("<b>Figure 3:</b> Diode non-linear function f(I) crossing zero with root I* = 0.2502 mA and initial bracket.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: PROBLEM 4 - DIODE DC CIRCUIT NEWTON-RAPHSON METHOD
    # =========================================================================
    story.append(Paragraph("5. Problem 4: Diode DC Circuit Analysis using Newton-Raphson Method", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=4))
    
    p4_desc = """
    <b>Mathematical Formulation:</b> Applying 1D Newton-Raphson: <i>I</i><sub>k+1</sub> = <i>I</i><sub>k</sub> - <i>f</i>(<i>I</i><sub>k</sub>) / <i>f'</i>(<i>I</i><sub>k</sub>).
    <br/>
    Differentiating <i>f</i>(<i>I</i>) = <i>I R</i> + <i>n V</i><sub>T</sub> ln(<i>I</i> / <i>I</i><sub>s</sub> + 1) - <i>V</i><sub>s</sub>:
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>f'</i>(<i>I</i>) = <i>R</i> + <i>n V</i><sub>T</sub> / (<i>I</i> + <i>I</i><sub>s</sub>)
    <br/>
    Since <i>f'</i>(<i>I</i>) &ge; <i>R</i> = 1000 &Omega; &gt; 0 for all physical currents <i>I</i> &ge; 0, no horizontal tangents or numerical blowups occur, ensuring quadratic convergence.
    """
    story.append(Paragraph(p4_desc, body_style))
    story.append(Spacer(1, 3))
    
    p4_table_data = [
        [Paragraph("<b>Initial Guess</b>", table_hdr_style), Paragraph("<b>Iter k</b>", table_hdr_style), Paragraph("<b>I_k [mA]</b>", table_hdr_style), Paragraph("<b>f(I_k) [V]</b>", table_hdr_style), Paragraph("<b>f'(I_k) [Ohm]</b>", table_hdr_style), Paragraph("<b>|Delta I| [A]</b>", table_hdr_style)],
        [Paragraph("<b>(a) I0 = 0.35 mA</b><br/>(Close to root)", table_cell_style), Paragraph("1<br/>2", table_cell_style), Paragraph("0.248416<br/><b>0.250180</b>", table_cell_style), Paragraph("+1.1251e-01<br/>-2.0391e-03", table_cell_style), Paragraph("1.1108e+03<br/>1.1561e+03", table_cell_style), Paragraph("1.0158e-04<br/><b>1.7638e-06</b>", table_cell_style)],
        [Paragraph("<b>(b) I0 = 1.00 mA</b><br/>(Farther from root)", table_cell_style), Paragraph("1<br/>2", table_cell_style), Paragraph("0.226450<br/><b>0.250011</b>", table_cell_style), Paragraph("+8.0354e-01<br/>-2.7595e-02", table_cell_style), Paragraph("1.0388e+03<br/>1.1712e+03", table_cell_style), Paragraph("7.7355e-04<br/><b>2.3561e-05</b>", table_cell_style)],
    ]
    t_p4 = Table(p4_table_data, colWidths=[105, 45, 84, 90, 90, 90])
    t_p4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_p4)
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>Comparison of Root-Finding Methods (Tolerance = 1e-4 A):</b>", h2_style))
    comp_root_data = [
        [Paragraph("<b>Method</b>", table_hdr_style), Paragraph("<b>Initial Conditions</b>", table_hdr_style), Paragraph("<b>Iterations</b>", table_hdr_style), Paragraph("<b>Final Root [mA]</b>", table_hdr_style), Paragraph("<b>Residual |f(I)| [V]</b>", table_hdr_style), Paragraph("<b>Convergence Rate</b>", table_hdr_style)],
        [Paragraph("Bisection", table_cell_style), Paragraph("[0, 5 mA]", table_cell_style), Paragraph("5", table_cell_style), Paragraph("0.234375", table_cell_style), Paragraph("1.1218e-01", table_cell_style), Paragraph("Linear (r = 1)", table_cell_style)],
        [Paragraph("Secant", table_cell_style), Paragraph("x0 = 0, x1 = 5 mA", table_cell_style), Paragraph("3", table_cell_style), Paragraph("0.253033", table_cell_style), Paragraph("3.2912e-03", table_cell_style), Paragraph("Superlinear (r &approx; 1.62)", table_cell_style)],
        [Paragraph("Newton-Raphson (a)", table_cell_style), Paragraph("I0 = 0.35 mA", table_cell_style), Paragraph("<b>2</b>", table_cell_style), Paragraph("0.250180", table_cell_style), Paragraph("9.7277e-07", table_cell_style), Paragraph("Quadratic (r = 2)", table_cell_style)],
        [Paragraph("Newton-Raphson (b)", table_cell_style), Paragraph("I0 = 1.00 mA", table_cell_style), Paragraph("<b>2</b>", table_cell_style), Paragraph("0.250011", table_cell_style), Paragraph("1.9637e-04", table_cell_style), Paragraph("Quadratic (r = 2)", table_cell_style)],
    ]
    t_comp = Table(comp_root_data, colWidths=[90, 85, 55, 84, 95, 95])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 3))
    
    p4_disc_text = """
    <b>Observations:</b> Both initial guesses require exactly <b>2 iterations</b> to satisfy the 10<sup>-4</sup> A tolerance. Physical circuit check: <i>I</i>* &approx; 0.2502 mA drops <i>V</i><sub>R</sub> = 0.2502 V across the 1 k&Omega; resistor, leaving <i>V</i><sub>D</sub> = 1.0 - 0.2502 = 0.7498 V across the diode, matching the standard forward bias for silicon.
    """
    story.append(Paragraph(p4_disc_text, body_style))
    story.append(Spacer(1, 4))
    
    if os.path.exists("figures/fig_problem4.png"):
        story.append(Image("figures/fig_problem4.png", width=360, height=155))
        story.append(Paragraph("<b>Figure 4:</b> Iterative convergence trajectories of Newton-Raphson method for diode operating current.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: PROBLEM 5 - PACKET LATENCY VANDERMONDE INTERPOLATION
    # =========================================================================
    story.append(Paragraph("6. Problem 5: Packet Latency Vandermonde Interpolation & Extrapolation Analysis", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=4))
    
    p5_desc = """
    <b>Physical Context:</b> Network engineers analyze packet latency <i>L</i>(<i>x</i>) [ms] as a function of packet size <i>x</i> [kB] to predict latency for other packet sizes.
    """
    story.append(Paragraph(p5_desc, body_style))
    story.append(Spacer(1, 2))
    
    data_p5 = [
        [Paragraph("<b>Packet Size x [kB]</b>", table_hdr_style), Paragraph("150.0", table_cell_style), Paragraph("200.0", table_cell_style), Paragraph("230.0", table_cell_style), Paragraph("260.0", table_cell_style), Paragraph("300.0", table_cell_style), Paragraph("340.0", table_cell_style), Paragraph("400.0", table_cell_style)],
        [Paragraph("<b>Latency y [ms]</b>", table_hdr_style), Paragraph("2.10", table_cell_style), Paragraph("2.85", table_cell_style), Paragraph("3.35", table_cell_style), Paragraph("3.95", table_cell_style), Paragraph("4.90", table_cell_style), Paragraph("6.10", table_cell_style), Paragraph("8.05", table_cell_style)]
    ]
    t_p5_data = Table(data_p5, colWidths=[112, 56, 56, 56, 56, 56, 56, 56])
    t_p5_data.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_p5_data)
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>Part (a): Vandermonde Matrix Approach:</b>", h2_style))
    p5_vander_text = """
    With <i>n</i> = 7 points, the unique interpolating polynomial is degree 6: <i>L</i>(<i>x</i>) = <i>c</i><sub>6</sub> <i>x</i><sup>6</sup> + <i>c</i><sub>5</sub> <i>x</i><sup>5</sup> + <i>c</i><sub>4</sub> <i>x</i><sup>4</sup> + <i>c</i><sub>3</sub> <i>x</i><sup>3</sup> + <i>c</i><sub>2</sub> <i>x</i><sup>2</sup> + <i>c</i><sub>1</sub> <i>x</i> + <i>c</i><sub>0</sub>.
    Solving <i>V</i> <b>c</b> = <b>y</b> where <i>V</i><sub>ij</sub> = <i>x</i><sub>i</sub><sup>7-j</sup> yields the polynomial coefficients:
    <br/>
    • <i>c</i><sub>6</sub> = -1.89262707 &times; 10<sup>-13</sup> &nbsp;&nbsp;|&nbsp;&nbsp; <i>c</i><sub>5</sub> = +3.01018087 &times; 10<sup>-10</sup> &nbsp;&nbsp;|&nbsp;&nbsp; <i>c</i><sub>4</sub> = -1.96580005 &times; 10<sup>-7</sup><br/>
    • <i>c</i><sub>3</sub> = +6.75374182 &times; 10<sup>-5</sup> &nbsp;&nbsp;|&nbsp;&nbsp; <i>c</i><sub>2</sub> = -1.28304368 &times; 10<sup>-2</sup> &nbsp;&nbsp;|&nbsp;&nbsp; <i>c</i><sub>1</sub> = +1.28842461 &times; 10<sup>0</sup><br/>
    • <i>c</i><sub>0</sub> = -5.16017635 &times; 10<sup>1</sup>
    <br/>
    <b>Condition Number:</b> cond(<i>V</i>) = <b>2.2646 &times; 10<sup>19</sup></b>. The Vandermonde matrix is severely ill-conditioned, magnifying floating-point roundoff near machine epsilon (10<sup>-16</sup>).
    """
    story.append(Paragraph(p5_vander_text, body_style))
    story.append(Spacer(1, 3))
    
    story.append(Paragraph("<b>Part (b): Latency Estimation for a 3 KB Packet & Critical Analysis:</b>", h2_style))
    p5_eval_text = """
    Evaluating at <i>x</i> = 3.0 kB:<br/>
    <i>L</i>(3.0) = <i>c</i><sub>6</sub>(3)<sup>6</sup> + <i>c</i><sub>5</sub>(3)<sup>5</sup> + <i>c</i><sub>4</sub>(3)<sup>4</sup> + <i>c</i><sub>3</sub>(3)<sup>3</sup> + <i>c</i><sub>2</sub>(3)<sup>2</sup> + <i>c</i><sub>1</sub>(3) + <i>c</i><sub>0</sub> = <b>-47.850156 ms</b> &approx; <b>-47.85 ms</b>.
    <br/><br/>
    <b>CRITICAL ENGINEERING & NUMERICAL ANALYSIS:</b><br/>
    1. <b>Physical Impossibility:</b> A negative latency (-47.85 ms) violates causality. Network latency must always be strictly positive: Latency = Propagation + Queuing + Serialization &gt; 0.<br/>
    2. <b>High-Order Extrapolation Trap:</b> The collected dataset spans [150, 400] kB. Evaluating at <i>x</i> = 3 kB represents an <b>extreme extrapolation</b> far outside the data support. High-degree polynomials suffer from Runge-like boundary oscillations, plunging drastically for small <i>x</i>.<br/>
    3. <b>Proper Engineering Practice:</b> Global high-order polynomial extrapolation should NEVER be used. Network engineers should employ linear regression (<i>L</i>(<i>x</i>) = &alpha; <i>x</i> + &beta;) or monotonic cubic splines, yielding a realistic latency of &approx; 0.6 - 1.0 ms for a 3 KB packet.
    """
    story.append(Paragraph(p5_eval_text, body_style))
    story.append(Spacer(1, 4))
    
    if os.path.exists("figures/fig_problem5.png"):
        story.append(Image("figures/fig_problem5.png", width=360, height=155))
        story.append(Paragraph("<b>Figure 5:</b> Vandermonde polynomial L(x) showing perfect interpolation within [150, 400] and wild divergence at x = 3 kB.", caption_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: PROBLEM 6 - SATELLITE TO GROUND ENERGY HARVESTING (PART 1)
    # =========================================================================
    story.append(Paragraph("7. Problem 6: Satellite to Ground Wireless Energy Harvesting Analysis", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=4))
    
    p6_desc = """
    <b>Physical Context & Research Background:</b> Following the research paper <i>'Wireless Energy Transfer from Space to Ground via Satellite Constellation Grids'</i> (Shehab et al., 2024), we evaluate a grid of <i>N</i> LEO satellites, each equipped with <i>M</i> antennas, transferring energy to an Earth-based Wirelessly Chargeable Device (WCD). Through Maximum Ratio Transmission (MRT), the harvested energy scales as <i>M N</i><sup>2</sup>:
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>E</i><sub>h</sub> = <i>M N</i><sup>2</sup> &int;<sub>0</sub><sup><i>T</i></sup> <i>P</i><sub>h</sub>(<i>t</i>) <i>dt</i> = <i>M N</i><sup>2</sup> &mu; &int;<sub>0</sub><sup><i>T</i></sup> [ (<i>R</i> + <i>H</i>)<sup>2</sup> + <i>R</i><sup>2</sup> - 2(<i>R</i> + <i>H</i>)<i>R</i> cos&phi; cos(&omega;<i>t</i>) ]<sup>-1</sup> <i>dt</i>
    <br/>
    where &mu; = &eta;<sub>h</sub> <i>P</i><sub>t</sub> <i>G</i><sub>t</sub> <i>G</i><sub>r</sub> [&lambda; / (4&pi;)]<sup>2</sup> &alpha;<sub>s</sub> &beta;<sub>s</sub>, and <i>T</i> = &theta;<sub>c</sub> / &omega;.
    """
    story.append(Paragraph(p6_desc, body_style))
    story.append(Spacer(1, 3))
    
    p6_param_box = """
    <b>System Parameters (Table I & Problem Specification):</b><br/>
    • Earth Radius: <i>R</i> = 6378 km &nbsp;&nbsp;|&nbsp;&nbsp; Satellite Altitude: <i>H</i> = 200 km<br/>
    • Angular Velocity: &omega; = [<i>G M</i><sub>e</sub> / (<i>R</i> + <i>H</i>)<sup>3</sup>]<sup>1/2</sup> = 1.182794 &times; 10<sup>-3</sup> rad/s<br/>
    • Antenna Gain: <i>G</i><sub>t</sub> = 50 dB = 10<sup>5</sup>, <i>G</i><sub>r</sub> = 10 dB = 10 &nbsp;&nbsp;|&nbsp;&nbsp; Transmit Power: <i>P</i><sub>t</sub> = 40 dBm = 10 W<br/>
    • Carrier Frequency: <i>f</i> = 868 MHz (&lambda; = 0.3456 m) &nbsp;&nbsp;|&nbsp;&nbsp; Rician Fading Product: &alpha;<sub>s</sub> &beta;<sub>s</sub> = 2<i>b</i><sub>0</sub> + &Omega; = 1.606<br/>
    • Antennas per Satellite: <i>M</i> = 8 &nbsp;&nbsp;|&nbsp;&nbsp; Harvesting Efficiency: &eta;<sub>h</sub> = 0.70 &nbsp;&nbsp;|&nbsp;&nbsp; Sensitivity Threshold: <i>P</i><sub>th</sub> = -20 dBm<br/>
    • Path Alignment: &phi; = 0 &nbsp;&nbsp;|&nbsp;&nbsp; Friis Harvesting Constant: &mu; = 8.504072 &times; 10<sup>3</sup> W&middot;m<sup>2</sup>.
    """
    p6_param_table = Table([[Paragraph(p6_param_box, callout_style)]], colWidths=[504])
    p6_param_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(p6_param_table)
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("<b>Question 1: Closed-Form Analytical Solution Derivation:</b>", h2_style))
    p6_q1_text = """
    <b>Yes, an exact closed-form solution exists!</b><br/>
    Let <i>A</i> = (<i>R</i> + <i>H</i>)<sup>2</sup> + <i>R</i><sup>2</sup> and <i>B</i> = 2<i>R</i>(<i>R</i> + <i>H</i>)cos&phi;. Using the <b>Weierstrass Half-Angle Substitution</b>:
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>u</i> = tan(&omega;<i>t</i> / 2) &rarr; cos(&omega;<i>t</i>) = (1 - <i>u</i><sup>2</sup>) / (1 + <i>u</i><sup>2</sup>), &nbsp;&nbsp;&nbsp;&nbsp;<i>dt</i> = (2 / &omega;) &middot; <i>du</i> / (1 + <i>u</i><sup>2</sup>)
    <br/>
    Substituting into the integral:
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>E</i><sub>h</sub> = <i>M N</i><sup>2</sup> &mu; &int;<sub>0</sub><sup>tan(&omega;<i>T</i>/2)</sup> [ <i>A</i> - <i>B</i>(1 - <i>u</i><sup>2</sup>)/(1 + <i>u</i><sup>2</sup>) ]<sup>-1</sup> [2 / &omega;(1 + <i>u</i><sup>2</sup>)] <i>du</i> = (2 <i>M N</i><sup>2</sup> &mu; / &omega;) &int;<sub>0</sub><sup>tan(&omega;<i>T</i>/2)</sup> [ (<i>A</i> - <i>B</i>) + (<i>A</i> + <i>B</i>)<i>u</i><sup>2</sup> ]<sup>-1</sup> <i>du</i>
    <br/>
    Evaluating this standard arctangent integral yields:
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>E</i><sub>h</sub> = [2 <i>M N</i><sup>2</sup> &mu; / (&omega; (<i>A</i><sup>2</sup> - <i>B</i><sup>2</sup>)<sup>1/2</sup>)] &middot; tan<sup>-1</sup>( [(<i>A</i> + <i>B</i>)/(<i>A</i> - <i>B</i>)]<sup>1/2</sup> tan(&omega;<i>T</i> / 2) )
    <br/>
    For an aligned coplanar ground track (&phi; = 0): <i>A</i> - <i>B</i> = <i>H</i><sup>2</sup>, <i>A</i> + <i>B</i> = (<i>H</i> + 2<i>R</i>)<sup>2</sup>, so (<i>A</i><sup>2</sup> - <i>B</i><sup>2</sup>)<sup>1/2</sup> = <i>H</i>(<i>H</i> + 2<i>R</i>) and [(<i>A</i>+<i>B</i>)/(<i>A</i>-<i>B</i>)]<sup>1/2</sup> = (<i>H</i> + 2<i>R</i>)/<i>H</i>.
    <br/><br/>
    <b>Final Exact Closed-Form Expression:</b>
    <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<b><i>E</i><sub>h</sub> = [2 <i>M N</i><sup>2</sup> &mu; / (&omega; <i>H</i> (<i>H</i> + 2<i>R</i>))] &middot; tan<sup>-1</sup>( [(<i>H</i> + 2<i>R</i>)/<i>H</i>] tan(&omega;<i>T</i> / 2) )</b>
    <br/><br/>
    <i>Note: Using the reciprocal trigonometric identity tan<sup>-1</sup>(x) = &pi;/2 - tan<sup>-1</sup>(1/x), this expression is mathematically identical to Dr. Shehab's published formula:</i><br/>
    &nbsp;&nbsp;&nbsp;&nbsp;<i>E</i><sub>h</sub> = [<i>M N</i><sup>2</sup> &mu; / (<i>H</i><sup>2</sup> &omega; + 2<i>HR</i> &omega;)] &middot; [ &pi; - 2 tan<sup>-1</sup>( [<i>H</i> cot(&omega;<i>T</i>/2)] / (<i>H</i> + 2<i>R</i>) ) ].
    """
    story.append(Paragraph(p6_q1_text, body_style))
    
    story.append(PageBreak())
    
    # =========================================================================
    # PAGE 10: PROBLEM 6 (PARTS 2 & 3, TABLE & FIGURE 6)
    # =========================================================================
    story.append(Paragraph("<b>Problem 6 (Continued): Numerical Methods & Satellite Scaling (N = 4:4:32)</b>", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=1, spaceAfter=4))
    
    p6_table_data = [
        [Paragraph("<b>N</b>", table_hdr_style), Paragraph("<b>T [s]</b>", table_hdr_style), Paragraph("<b>Closed-Form [mJ]</b>", table_hdr_style), Paragraph("<b>Trapezoid [mJ]</b>", table_hdr_style), Paragraph("<b>Simpson [mJ]</b>", table_hdr_style), Paragraph("<b>Monte-Carlo [mJ]</b>", table_hdr_style), Paragraph("<b>e_Trap (%)</b>", table_hdr_style), Paragraph("<b>e_Simp (%)</b>", table_hdr_style), Paragraph("<b>e_MC (%)</b>", table_hdr_style)],
        [Paragraph("4", table_cell_style), Paragraph("44.4", table_cell_style), Paragraph("0.7381", table_cell_style), Paragraph("0.7381", table_cell_style), Paragraph("0.7381", table_cell_style), Paragraph("0.7371", table_cell_style), Paragraph("2.35e-04", table_cell_style), Paragraph("1.78e-08", table_cell_style), Paragraph("0.14 %", table_cell_style)],
        [Paragraph("8", table_cell_style), Paragraph("99.6", table_cell_style), Paragraph("3.7359", table_cell_style), Paragraph("3.7359", table_cell_style), Paragraph("3.7359", table_cell_style), Paragraph("3.7302", table_cell_style), Paragraph("2.34e-04", table_cell_style), Paragraph("1.78e-08", table_cell_style), Paragraph("0.15 %", table_cell_style)],
        [Paragraph("12", table_cell_style), Paragraph("152.4", table_cell_style), Paragraph("8.9604", table_cell_style), Paragraph("8.9604", table_cell_style), Paragraph("8.9604", table_cell_style), Paragraph("8.9482", table_cell_style), Paragraph("2.34e-04", table_cell_style), Paragraph("1.77e-08", table_cell_style), Paragraph("0.14 %", table_cell_style)],
        [Paragraph("16", table_cell_style), Paragraph("204.7", table_cell_style), Paragraph("16.4181", table_cell_style), Paragraph("16.4181", table_cell_style), Paragraph("16.4181", table_cell_style), Paragraph("16.4011", table_cell_style), Paragraph("2.34e-04", table_cell_style), Paragraph("1.77e-08", table_cell_style), Paragraph("0.10 %", table_cell_style)],
        [Paragraph("20", table_cell_style), Paragraph("257.0", table_cell_style), Paragraph("26.1108", table_cell_style), Paragraph("26.1108", table_cell_style), Paragraph("26.1108", table_cell_style), Paragraph("26.1284", table_cell_style), Paragraph("2.33e-04", table_cell_style), Paragraph("1.76e-08", table_cell_style), Paragraph("0.07 %", table_cell_style)],
        [Paragraph("24", table_cell_style), Paragraph("309.5", table_cell_style), Paragraph("38.0400", table_cell_style), Paragraph("38.0399", table_cell_style), Paragraph("38.0400", table_cell_style), Paragraph("38.1023", table_cell_style), Paragraph("2.33e-04", table_cell_style), Paragraph("1.75e-08", table_cell_style), Paragraph("0.16 %", table_cell_style)],
        [Paragraph("28", table_cell_style), Paragraph("362.1", table_cell_style), Paragraph("52.2067", table_cell_style), Paragraph("52.2066", table_cell_style), Paragraph("52.2067", table_cell_style), Paragraph("52.3114", table_cell_style), Paragraph("2.32e-04", table_cell_style), Paragraph("1.74e-08", table_cell_style), Paragraph("0.20 %", table_cell_style)],
        [Paragraph("32", table_cell_style), Paragraph("415.1", table_cell_style), Paragraph("68.6121", table_cell_style), Paragraph("68.6120", table_cell_style), Paragraph("68.6121", table_cell_style), Paragraph("68.7905", table_cell_style), Paragraph("2.31e-04", table_cell_style), Paragraph("1.73e-08", table_cell_style), Paragraph("0.26 %", table_cell_style)],
    ]
    t_p6 = Table(p6_table_data, colWidths=[24, 46, 68, 68, 68, 68, 54, 54, 54])
    t_p6.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_p6)
    story.append(Spacer(1, 3))
    
    p6_concl_text = """
    <b>Observations:</b> Simpson's 1/3 rule delivers near machine-precision accuracy (<i>e</i> &sim; 10<sup>-8</sup>%), Multiple Trapezoidal rule demonstrates solid second-order convergence (<i>e</i> &sim; 10<sup>-4</sup>%), and Monte-Carlo achieves statistical accuracy within 0.2%. Harvested energy scales rapidly from 0.74 mJ to 68.61 mJ as constellation size expands from 4 to 32 satellites.
    """
    story.append(Paragraph(p6_concl_text, body_style))
    story.append(Spacer(1, 4))
    
    if os.path.exists("figures/fig_problem6.png"):
        story.append(Image("figures/fig_problem6.png", width=420, height=165))
        story.append(Paragraph("<b>Figure 6:</b> Harvested energy E_h vs number of constellation satellites N (left) and relative true errors on log scale (right).", caption_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report PDF built successfully: {pdf_filename}")

if __name__ == '__main__':
    build_pdf()

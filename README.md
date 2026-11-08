# MATH502: Numerical Methods Coursework

**German University in Cairo (GUC)**  
**Faculty of Information Engineering and Technology (IET)**  
**Course:** MATH502 - Numerical Methods / Scientific Computing  
**Instructor:** Dr. Mohammad Shehab  
**Teaching Assistant:** Eng. Bahaaeldin Ibrahim (`bahaaeldin.ibrahim@guc.edu.eg`)  
**Students:** Mazen Altelbany (64-12371, Tutorial: T-04) & Yahia Talaat (64-3581, Tutorial: T-02)

---

## Repository Structure

```
MATH502-Numerical-Methods/
├── MATH502_Assignment1_Submission/         # Official submission package
│   ├── MATH502_Assignment1_Report.pdf      # 10-page formal report (PDF)
│   ├── run_all.m                           # Master MATLAB execution script
│   ├── Problem1_LORAN.m                    # 2D Newton-Raphson LORAN hyperbola solver (from scratch)
│   ├── Problem2_RSSI.m                     # Newton divided difference & Horner's scheme (from scratch)
│   ├── Problem3_Diode_Bisection_Secant.m   # Diode DC circuit (Bisection & Secant from scratch)
│   ├── Problem4_Diode_Newton.m             # Diode DC circuit (Newton-Raphson from scratch)
│   ├── Problem5_Packet_Latency.m           # Custom Vandermonde & Gaussian Elimination solver
│   ├── Problem6_Satellite_Energy_Harvesting.m # Custom Trapezoid, Simpson, Monte-Carlo quadrature
│   └── README.md                           # Package instructions and policy
├── assignment 1/
│   └── Assignment 1.pdf                    # Assignment 1 problem sheet
├── figures/                                # High-resolution figures used in the report
│   ├── fig_problem1.png                    # LORAN hyperbolic curves and Newton trajectory
│   ├── fig_problem2.png                    # RSSI data, Newton polynomial, and 5m evaluation
│   ├── fig_problem3.png                    # Diode non-linear function f(I) and root bracket
│   ├── fig_problem4.png                    # Diode Newton-Raphson convergence comparison
│   ├── fig_problem5.png                    # Packet latency interpolation & extrapolation divergence
│   └── fig_problem6.png                    # Harvested energy scaling & quadrature relative true errors
├── shehab_paper.pdf                        # Primary research paper (Dr. Mohammad Shehab, IEEE)
├── generate_pdf_report.py                  # ReportLab script generating the official PDF report
├── generate_comprehensive_pdf.py           # ReportLab script generating the solutions guide
└── README.md                               # Repository overview and documentation
```

---

## Assignment 1 Problems & Key Results Summary

All numerical methods are implemented **from first principles** using `for` loops, `while` loops, and `if` conditions without any built-in black-box solvers.

| Problem | Method / Topic | Custom Algorithmic Details | Key Results |
| :--- | :--- | :--- | :--- |
| **Problem 1: LORAN Positioning** | 2D Newton-Raphson Non-linear System | Evaluates 2D residuals & Jacobian, solves 2x2 system via custom Cramer's rule / Gaussian elimination (no `\`, no `fsolve`). | Converges in 4 iterations to x* = [254.2211, 219.3070]^T from x_0 = [200, 200]^T (residual < 1e-14). |
| **Problem 2: WSN RSSI Interpolation** | Newton Divided Differences & Horner Scheme | Builds divided differences via nested loops, evaluates at 5m via Horner backward loop, and expands to monomial standard form via synthetic polynomial multiplication loops (no `polyfit`, no `polyval`). | P_4(5) = -57.4545 dBm. 0.45 dB discrepancy with -57.0 dBm analyzed (multipath fading, shadowing). Horner uses 4 mults + 8 adds/subs. |
| **Problem 3: Diode DC Circuit** | Bisection & Secant Root-Finding | Solves Shockley KVL equation using custom `while` loops and interval-updating `if` conditions (no `fzero`). | Solved on [0, 5 mA] for tolerance 1e-4 A. Bisection requires 5 iters (0.2344 mA); Secant requires 3 iters (0.2530 mA). Root I* = 0.250181 mA. |
| **Problem 4: Diode Newton-Raphson** | 1D Newton-Raphson Method | Evaluates f(I) and f'(I) analytically, updates step size delta = -f/f' inside a `while` loop with convergence checks. | Converges in only 2 iterations for both I_0 = 0.35 mA and I_0 = 1.0 mA to I* = 0.2502 mA (V_D = 0.7498 V). Quadratic convergence confirmed. |
| **Problem 5: Packet Latency** | Vandermonde Interpolation & Runge Analysis | Constructs Vandermonde matrix via nested `for` loops, solves linear system using **Gaussian Elimination with Partial Pivoting** (`for` loops and `if` conditions), and evaluates via custom Horner loop (no `vander`, no `\`, no `polyval`). | Degree-6 polynomial from 7 points. cond(V) = 2.26 x 10^19. Model predicts -47.85 ms at 3 KB (extrapolation trap & Runge divergence). |
| **Problem 6: Satellite WET** | Analytical Closed Form & Numerical Quadrature | Implements Multiple Trapezoidal via accumulation loop, Simpson's 1/3 via loop with odd/even conditionals, and Monte-Carlo via sampling loop (no `trapz`, `integral`, or `mean`). | Closed-form derived via Weierstrass substitution u = tan(omega*t / 2) with symmetric 2x transit window. Evaluated for N = 4:4:32 satellites. Simpson 1/3 error ~ 10^-8 %, Trapezoidal error ~ 10^-4 %, Monte-Carlo error ~ 0.2 - 2.8 %. |

---

## How to Run the MATLAB Scripts

In MATLAB, change directory to `MATH502_Assignment1_Submission`:

```matlab
cd MATH502_Assignment1_Submission

% Run all problems sequentially:
run_all

% Or run individual scripts:
Problem1_LORAN
Problem2_RSSI
Problem3_Diode_Bisection_Secant
Problem4_Diode_Newton
Problem5_Packet_Latency
Problem6_Satellite_Energy_Harvesting
```

---

## Implementation Policy & Language Justification
In accordance with course and TA guidelines, **MATLAB (MathWorks R2026a)** was chosen with a strict first-principles implementation policy:
1. **Full Transparency:** Every numerical step (forward elimination, back substitution, divided differences, Horner evaluation, bracket reduction, Secant interpolation, Newton update, and composite quadrature) is written explicitly using `for` loops, `while` loops, and `if` conditions.
2. **Zero Black-Box Solvers:** Built-in numerical solvers such as `fsolve`, `fzero`, `vander`, `polyfit`, `polyval`, `trapz`, or matrix backslash `\` are not used for any problem solution.
3. **High-Precision IEEE 754 Arithmetic:** Native double-precision floating-point arithmetic enables accurate tracking of algorithm convergence and conditioning.

---

## Formal Reports
The formal student reports are available at:  
- [**`MATH502_Assignment1_Report_Final.pdf`**](MATH502_Assignment1_Report_Final.pdf) (Official final submission report)  
- [**`MATH502_Assignment1_Solutions_and_Code_Guide.pdf`**](MATH502_Assignment1_Solutions_and_Code_Guide.pdf) (23-page comprehensive solution & code guide)

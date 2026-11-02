# MATH502: Numerical Methods Coursework

**German University in Cairo (GUC)**  
**Faculty of Information Engineering and Technology (IET)**  
**Course:** MATH502 — Numerical Methods / Scientific Computing  
**Instructor:** Dr. Mohammad Shehab  
**Teaching Assistant:** Eng. Bahaaeldin Ibrahim (`bahaaeldin.ibrahim@guc.edu.eg`)  
**Students:** Mazen Altelbany (64-12371) & Yahia Talaat (64-3581)

---

## 📁 Repository Structure

```
MATH502-Numerical-Methods/
├── MATH502_Assignment1_Submission/         # Official submission package
│   ├── MATH502_Assignment1_Report.pdf      # 10-page formal report (PDF)
│   ├── run_all.m                           # Master MATLAB execution script
│   ├── Problem1_LORAN.m                    # 2D Newton-Raphson LORAN hyperbola solver
│   ├── Problem2_RSSI.m                     # Newton divided difference & Horner's scheme
│   ├── Problem3_Diode_Bisection_Secant.m   # Diode DC circuit (Bisection & Secant)
│   ├── Problem4_Diode_Newton.m             # Diode DC circuit (Newton-Raphson)
│   ├── Problem5_Packet_Latency.m           # Vandermonde matrix interpolation & extrapolation analysis
│   ├── Problem6_Satellite_Energy_Harvesting.m # Satellite WET closed form & quadrature methods
│   └── README.md                           # Package instructions and language justification
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
└── README.md                               # Repository overview and documentation
```

---

## 📊 Assignment 1 Problems & Key Results Summary

| Problem | Method / Topic | Key Results | MATLAB Built-in Validation |
| :--- | :--- | :--- | :--- |
| **Problem 1: LORAN Positioning** | 2D Newton-Raphson Non-linear System | Converges in 4 iterations to $\mathbf{x}^* = [254.2211, 219.3070]^T$ from $\mathbf{x}_0 = [200, 200]^T$. 4 hyperbola intersection roots analyzed. | Validated against `fsolve` (residual $< 10^{-14}$) |
| **Problem 2: WSN RSSI Interpolation** | Newton Divided Differences & Horner Scheme | $P_4(5) = -57.4545\text{ dBm}$. $0.45\text{ dB}$ discrepancy with $-57.0\text{ dBm}$ analyzed (multipath fading, shadowing). Horner uses 4 mults + 8 adds/subs. | Verified via `polyfit` and `polyval` |
| **Problem 3: Diode DC Circuit** | Bisection & Secant Root-Finding | Shockley KVL equation solved on $[0, 5\text{ mA}]$ for $\epsilon = 10^{-4}\text{ A}$. Bisection requires 5 iters ($0.2344\text{ mA}$); Secant requires 3 iters ($0.2530\text{ mA}$). | Validated against `fzero` ($I^* = 0.250181\text{ mA}$) |
| **Problem 4: Diode Newton-Raphson** | 1D Newton-Raphson Method | Converges in only 2 iterations for both $I_0 = 0.35\text{ mA}$ and $I_0 = 1.0\text{ mA}$ to $I^* = 0.2502\text{ mA}$ ($V_D = 0.7498\text{ V}$). | Quadratic convergence confirmed |
| **Problem 5: Packet Latency** | Vandermonde Interpolation & Runge Analysis | Degree-6 polynomial from 7 points. $\text{cond}(V) = 2.26 \times 10^{19}$. Model predicts $-47.85\text{ ms}$ at $3\text{ KB}$ (extrapolation trap & Runge divergence). | Solved via `V \ y` and verified with `polyval` |
| **Problem 6: Satellite WET** | Analytical Closed Form & Numerical Quadrature | Closed-form derived via Weierstrass substitution $u = \tan(\omega t / 2)$. Evaluated for $N = 4:4:32$ satellites. Simpson 1/3 error $\sim 10^{-8}\%$, Trapezoidal error $\sim 10^{-4}\%$, Monte-Carlo error $\sim 0.1-0.5\%$. | Compared against `trapz` and exact analytical form |

---

## 🚀 How to Run the MATLAB Scripts

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

## 🛠️ Programming Language Justification
In accordance with course guidelines, **MATLAB (MathWorks R2026a)** was chosen as the single programming language:
1. Native support for linear algebra, matrix inversion, and vectorization (`\`, `.*`, `./`).
2. Robust, production-grade built-in solvers (`fsolve`, `fzero`, `vander`, `polyfit`, `polyval`, `trapz`) used to benchmark student implementations.
3. High-precision IEEE 754 double precision arithmetic and publication-ready plotting tools.

---

## 📄 Formal Report
The complete 10-page formal student report is available at:  
[**`MATH502_Assignment1_Report.pdf`**](MATH502_Assignment1_Submission/MATH502_Assignment1_Report.pdf)


# MATH502: Numerical Methods — Assignment 1 Submission Package
**German University in Cairo (GUC)**  
**Faculty of Information Engineering and Technology (IET)**  
**Course:** MATH502 — Numerical Methods / Scientific Computing  
**Instructor:** Dr. Mohammad Shehab  
**Teaching Assistant:** Eng. Bahaaeldin Ibrahim (`bahaaeldin.ibrahim@guc.edu.eg`)  

---

## 👥 Student Details
- **Student 1 Name:** Mazen Altelbany
- **Student 1 ID:** 64-12371 (Faculty of IET, GUC, Tutorial: T-04)
- **Student 2 Name:** Yahia Talaat
- **Student 2 ID:** 64-3581 (Faculty of IET, GUC, Tutorial: T-02)

---

## 📁 Package Contents

| File Name | Description |
| :--- | :--- |
| **`MATH502_Assignment1_Report.pdf`** | Formal student report with cover page, language justification, mathematical derivations, manual pen-and-paper iterations, code listings, result tables, and plots. |
| **`run_all.m`** | Master MATLAB script that runs all six problem scripts sequentially and prints formatted outputs. |
| **`Problem1_LORAN.m`** | Script solving the LORAN 2D non-linear hyperbola system via Newton-Raphson and verifying against built-in `fsolve`. |
| **`Problem2_RSSI.m`** | Script computing Newton's divided difference table, evaluating at 5m, comparing against -57 dBm, and presenting Horner's form. |
| **`Problem3_Diode_Bisection_Secant.m`** | Script solving the Shockley diode DC equation using Bisection and Secant methods, and validating against `fzero`. |
| **`Problem4_Diode_Newton.m`** | Script solving the diode equation using 1D Newton-Raphson for initial guesses $I_0 = 0.35\text{ mA}$ and $I_0 = 1.0\text{ mA}$. |
| **`Problem5_Packet_Latency.m`** | Script constructing the Vandermonde matrix, solving for polynomial coefficients via matrix left division `\`, evaluating at 3 KB, and analyzing extrapolation failure. |
| **`Problem6_Satellite_Energy_Harvesting.m`** | Script evaluating satellite WET integral analytically (closed-form) and numerically (Multiple Trapezoidal, Simpson's 1/3, Monte-Carlo) with true error comparison for $N = 4:4:32$. |

---

## 🚀 How to Run the MATLAB Scripts

### Option 1: Run All Problems via Master Script
In MATLAB, navigate to this directory and type in the Command Window:
```matlab
run_all
```

### Option 2: Run Individual Problem Scripts
You can run any problem independently:
```matlab
Problem1_LORAN
Problem2_RSSI
Problem3_Diode_Bisection_Secant
Problem4_Diode_Newton
Problem5_Packet_Latency
Problem6_Satellite_Energy_Harvesting
```

---

## 🛠️ Justification of Programming Language (MATLAB)
MATLAB (MathWorks) was chosen as the single programming language for this assignment for the following key reasons:
1. **Industry and Academic Standard:** MATLAB is the benchmark platform for engineering mathematics, numerical analysis, and signal processing.
2. **Native Vectorization & Matrix Operations:** Direct algebraic syntax for matrix inversion, solving linear systems (`\`), and element-wise computations (`.*`, `./`).
3. **High-Performance Built-in Numerical Solvers:** Includes specialized, production-tested numerical routines such as `fsolve`, `fzero`, `vander`, `polyfit`, `polyval`, and `trapz` used to validate and benchmark the custom student implementations.
4. **Precision and Visualization:** Built-in double-precision floating-point arithmetic compliant with IEEE 754 and publication-quality 2D/3D visualization capabilities.

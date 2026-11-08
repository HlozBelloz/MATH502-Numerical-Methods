# MATH502: Numerical Methods - Assignment 1 Submission Package
**German University in Cairo (GUC)**  
**Faculty of Information Engineering and Technology (IET)**  
**Course:** MATH502 - Numerical Methods / Scientific Computing  
**Instructor:** Dr. Mohammad Shehab  
**Teaching Assistant:** Eng. Bahaaeldin Ibrahim (`bahaaeldin.ibrahim@guc.edu.eg`)  

---

## Student Details
- **Student 1 Name:** Mazen Altelbany
- **Student 1 ID:** 64-12371 (Faculty of IET, GUC, Tutorial: T-04)
- **Student 2 Name:** Yahia Talaat
- **Student 2 ID:** 64-3581 (Faculty of IET, GUC, Tutorial: T-02)

---

## Package Contents

All algorithms are implemented **100% from first principles** using explicit control structures (`for` loops, `while` loops, and `if` conditions). No built-in numerical solvers, toolboxes, or high-level library routines (such as `fsolve`, `fzero`, `vander`, backslash `\`, `polyfit`, `polyval`, or `trapz`) are used for the solutions.

| File Name | Description |
| :--- | :--- |
| **`MATH502_Assignment1_Report.pdf`** | Formal student report with cover page, language justification, mathematical derivations, manual pen-and-paper iterations, code listings, result tables, and plots. |
| **`run_all.m`** | Master MATLAB script that runs all six problem scripts sequentially and prints formatted outputs. |
| **`Problem1_LORAN.m`** | Script solving the LORAN 2D non-linear hyperbola system via Newton-Raphson from first principles, solving the 2x2 Jacobian system with custom Cramer's rule / Gaussian elimination and direct residual checks (no `fsolve`, no `\`). |
| **`Problem2_RSSI.m`** | Script computing Newton's divided difference table via nested loops, evaluating at 5m via Horner's backward loop, and expanding to standard monomial form via synthetic polynomial multiplication loops (no `polyfit`, no `polyval`). |
| **`Problem3_Diode_Bisection_Secant.m`** | Script solving the Shockley diode DC equation using pure `while` loops and `if` conditions for Bisection and Secant methods (no `fzero`). |
| **`Problem4_Diode_Newton.m`** | Script solving the diode equation using a pure `while` loop 1D Newton-Raphson method with analytical derivatives and quadratic convergence checks. |
| **`Problem5_Packet_Latency.m`** | Script constructing the Vandermonde matrix via nested loops, solving for polynomial coefficients via custom **Gaussian Elimination with Partial Pivoting** (`for` loops and `if` conditions), and evaluating via a custom Horner loop (no `vander`, no `\`, no `polyval`). |
| **`Problem6_Satellite_Energy_Harvesting.m`** | Script evaluating satellite WET integral analytically (closed-form) and numerically (Multiple Trapezoidal via accumulation loop, Simpson's 1/3 via loop with odd/even conditionals, and Monte-Carlo via sampling loop) without built-in `trapz`, `integral`, or `mean`. |

---

## How to Run the MATLAB Scripts

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

## Implementation Policy & Language Justification (MATLAB)
In accordance with course and TA instructions:
1. **Algorithmic Transparency:** All numerical methods are coded explicitly from fundamental mathematical definitions using `for` loops, `while` loops, and `if` conditionals, demonstrating complete understanding of the underlying algorithmic mechanics.
2. **No Black-Box Solvers:** High-level built-in black-box functions (e.g., `fsolve`, `fzero`, `vander`, `polyfit`, `polyval`, `trapz`, or matrix backslash `\`) are strictly avoided in all problem solutions.
3. **Double-Precision Arithmetic:** MATLAB provides standard IEEE 754 double precision floating-point numbers, ensuring reliable tracking of roundoff errors, tolerances, and ill-conditioning effects.

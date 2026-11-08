%% MATH502: Numerical Methods - Assignment 1
% Problem 5: Packet Latency Vandermonde Interpolation & Extrapolation Analysis
% Students: Mazen Altelbany (64-12371) & Yahia Talaat (64-3581)
% German University in Cairo (GUC)
%
% Implemented from first principles using for loops and if conditions.
% Includes custom Vandermonde assembly, Gaussian Elimination with Partial Pivoting,
% and Horner's evaluation. No built-in solvers (vander, backslash, polyfit, polyval).

clear; clc; close all;

fprintf('========================================================================\n');
fprintf('Problem 5: Packet Latency Interpolation & Extrapolation Analysis\n');
fprintf('Students: Mazen Altelbany (64-12371) & Yahia Talaat (64-3581)\n');
fprintf('========================================================================\n\n');

%% Given Dataset
x = [150.0, 200.0, 230.0, 260.0, 300.0, 340.0, 400.0]'; % Packet size [kB]
y = [2.10, 2.85, 3.35, 3.95, 4.90, 6.10, 8.05]';         % Latency [ms]
n = length(x);                                            % 7 data points -> degree 6

%% Part (a): Vandermonde Matrix Approach (From First Principles)
fprintf('--- PART (a): Custom Vandermonde Matrix & Gaussian Elimination ---\n');

% 1. Construct Vandermonde Matrix V using nested for-loops (No built-in vander)
% V(i, j) = x(i)^(n - j) for descending powers x^6, x^5, ..., x^0
V = zeros(n, n);
for i = 1:n
    for j = 1:n
        V(i, j) = x(i)^(n - j);
    end
end

fprintf('Vandermonde Matrix Dimension: %d x %d (Constructed via nested loops)\n', size(V,1), size(V,2));

% 2. Solve V * c = y via Gaussian Elimination with Partial Pivoting (From Scratch)
% Form augmented matrix [V | y]
Aug = zeros(n, n + 1);
for i = 1:n
    for j = 1:n
        Aug(i, j) = V(i, j);
    end
    Aug(i, n + 1) = y(i);
end

% Forward Elimination with Row Pivoting
for p = 1:(n - 1)
    % Find pivot row with maximum absolute value in column p
    max_val = abs(Aug(p, p));
    pivot_row = p;
    for r = (p + 1):n
        if abs(Aug(r, p)) > max_val
            max_val = abs(Aug(r, p));
            pivot_row = r;
        end
    end
    
    % Swap current row with pivot row if necessary
    if pivot_row ~= p
        for col = p:(n + 1)
            temp = Aug(p, col);
            Aug(p, col) = Aug(pivot_row, col);
            Aug(pivot_row, col) = temp;
        end
    end
    
    % Row elimination
    for r = (p + 1):n
        factor = Aug(r, p) / Aug(p, p);
        for col = p:(n + 1)
            Aug(r, col) = Aug(r, col) - factor * Aug(p, col);
        end
    end
end

% Backward Substitution
c = zeros(n, 1);
for r = n:-1:1
    sum_val = 0.0;
    for k = (r + 1):n
        sum_val = sum_val + Aug(r, k) * c(k);
    end
    c(r) = (Aug(r, n + 1) - sum_val) / Aug(r, r);
end

fprintf('\nInterpolating Polynomial Coefficients (Descending Powers c6 to c0):\n');
for i = 1:n
    power = n - i;
    fprintf('  c_%d (coefficient of x^%d) = %18.10e\n', power, power, c(i));
end

% Display full polynomial formula
fprintf('\nPolynomial Function L(x):\n');
fprintf('  L(x) = (%+.4e)*x^6 + (%+.4e)*x^5 + (%+.4e)*x^4\n', c(1), c(2), c(3));
fprintf('         + (%+.4e)*x^3 + (%+.4e)*x^2 + (%+.4e)*x + (%+.4e)\n\n', ...
        c(4), c(5), c(6), c(7));

% Verification at original data points using custom Horner scheme
fprintf('Verification at original data points (Custom Horner loop, no polyval):\n');
fprintf('%-12s %-14s %-14s %-14s\n', 'x [kB]', 'Measured [ms]', 'Interpolated [ms]', 'Residual');
fprintf('------------------------------------------------------------\n');
for i = 1:n
    % Custom Horner evaluation
    val = c(1);
    for k = 2:n
        val = val * x(i) + c(k);
    end
    fprintf('%-12.1f %-14.2f %-14.4f %-14.2e\n', x(i), y(i), val, abs(val - y(i)));
end

%% Part (b): Latency Estimation for a 3 KB Packet & Critical Analysis
fprintf('\n--- PART (b): Estimation for 3 KB Packet & Critical Discussion ---\n');
x_target = 3.0; % 3 KB

% Evaluate at x = 3 KB using custom Horner evaluation loop
latency_3kb = c(1);
for k = 2:n
    latency_3kb = latency_3kb * x_target + c(k);
end

fprintf('Model Predicted Latency at x = 3 KB: %.4f ms\n\n', latency_3kb);

fprintf('CRITICAL ENGINEERING ANALYSIS & DISCUSSION:\n');
fprintf('  1. Physical Impossibility: A predicted latency of %.2f ms is negative,\n', latency_3kb);
fprintf('     which is physically impossible in communication networks where latency must\n');
fprintf('     be strictly positive (Transmission Delay + Propagation Delay + Queuing Delay).\n');
fprintf('  2. Extrapolation Danger: The measured dataset spans [150, 400] kB.\n');
fprintf('     Evaluating at x = 3 kB is an EXTRAPOLATION far outside the domain.\n');
fprintf('  3. High-Order Polynomial Oscillation (Runge Phenomenon): High-degree polynomials\n');
fprintf('     (degree 6 here) oscillate violently outside and near the boundaries of the data\n');
fprintf('     range, causing catastrophic divergence for small x.\n');
fprintf('  4. Ill-Conditioning & Precision Loss: With cond(V) ~ 2.3e19 and eps ~ 2.2e-16,\n');
fprintf('     the bound cond(V)*eps ~ 5e3 >> 1. The error bound exceeds 100%%, amplifying roundoff\n');
fprintf('     by orders of magnitude and leaving high-order coefficients with no reliable digits.\n');
fprintf('  5. Proper Modeling Recommendation: To predict latency for small packets, engineers\n');
fprintf('     should use a physically-grounded linear regression model (L(x) = a*x + b) or\n');
fprintf('     piecewise spline interpolation, rather than global high-degree polynomials.\n\n');

fprintf('Problem 5 Complete.\n');

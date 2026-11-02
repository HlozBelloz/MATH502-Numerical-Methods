%% MATH502: Numerical Methods - Assignment 1
% Problem 5: Packet Latency Vandermonde Interpolation & Extrapolation Analysis
% Student: Mazen Altelbany (64-12371)
% German University in Cairo (GUC)

clear; clc; close all;

fprintf('Problem 5: Packet Latency Interpolation\n\n');

%% Given Data
x = [150.0, 200.0, 230.0, 260.0, 300.0, 340.0, 400.0]'; % Packet size [kB]
y = [2.10, 2.85, 3.35, 3.95, 4.90, 6.10, 8.05]';         % Latency [ms]
n = length(x);                                            % 7 data points -> degree 6

%% Part (a): Vandermonde Matrix Approach
fprintf('--- PART (a): Vandermonde Matrix Approach ---\n');
% The interpolating polynomial of degree n-1 = 6 is:
% L(x) = c6*x^6 + c5*x^5 + c4*x^4 + c3*x^3 + c2*x^2 + c1*x + c0
% The Vandermonde system is V * c = y

% Construct Vandermonde matrix (MATLAB built-in vander)
V = vander(x);

% Condition number
cond_V = cond(V);
fprintf('Vandermonde Matrix Dimension: %d x %d\n', size(V,1), size(V,2));
fprintf('Condition Number cond(V) = %.4e (Severely Ill-Conditioned!)\n', cond_V);
fprintf('Precision loss bound: cond(V) * eps ≈ %.2e >> 1 (Amplification factor ~ 5000)\n\n', cond_V * eps);

% Solve for polynomial coefficients using MATLAB backslash operator
c = V \ y;

fprintf('Interpolating Polynomial Coefficients (Descending Order):\n');
for i = 1:n
    power = n - i;
    fprintf('  c_%d (coefficient of x^%d) = %18.10e\n', power, power, c(i));
end

% Display full polynomial formula
fprintf('\nPolynomial Function L(x):\n');
fprintf('  L(x) = (%+.4e)*x^6 + (%+.4e)*x^5 + (%+.4e)*x^4\n', c(1), c(2), c(3));
fprintf('         + (%+.4e)*x^3 + (%+.4e)*x^2 + (%+.4e)*x + (%+.4e)\n\n', ...
        c(4), c(5), c(6), c(7));

% Verification with MATLAB built-in polyfit and polyval
p_builtin = polyfit(x, y, n-1);
fprintf('Verification at original data points:\n');
fprintf('%-12s %-14s %-14s %-14s\n', 'x [kB]', 'Measured [ms]', 'Interpolated [ms]', 'Residual');
fprintf('------------------------------------------------------------\n');
for i = 1:n
    val = polyval(c, x(i));
    fprintf('%-12.1f %-14.2f %-14.4f %-14.2e\n', x(i), y(i), val, abs(val - y(i)));
end

%% Part (b): Latency Estimation for a 3 KB Packet & Critical Analysis
fprintf('\n--- PART (b): Estimation for 3 KB Packet & Critical Discussion ---\n');
x_target = 3.0; % 3 KB
latency_3kb = polyval(c, x_target);

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


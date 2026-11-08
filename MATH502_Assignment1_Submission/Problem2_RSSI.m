%% MATH502: Numerical Methods - Assignment 1
% Problem 2: Wireless Sensor Network (WSN) RSSI Interpolation
% Students: Mazen Altelbany (64-12371) & Yahia Talaat (64-3581)
% German University in Cairo (GUC)
%
% Implemented from first principles using for loops and if conditions.
% No built-in interpolation or polynomial fitting functions used.

clear; clc; close all;

fprintf('========================================================================\n');
fprintf('Problem 2: WSN RSSI Interpolation (Newton Form & Horner Scheme)\n');
fprintf('Students: Mazen Altelbany (64-12371) & Yahia Talaat (64-3581)\n');
fprintf('========================================================================\n\n');

%% Given Dataset
d = [1.0, 2.5, 4.0, 6.0, 8.0]';      % Distance [m]
RSSI = [-40.0, -47.0, -54.0, -60.0, -66.0]'; % RSSI [dBm]
n = length(d);

%% Part (a): Newton's Divided Difference Table & Polynomial
fprintf('--- PART (a): Newton Divided Difference Table (Nested for-loops) ---\n');
DTable = zeros(n, n);

% Initialize first column with f[x_i] = RSSI
for i = 1:n
    DTable(i, 1) = RSSI(i);
end

% Compute divided differences column by column
for j = 2:n
    for i = 1:(n - j + 1)
        delta_f = DTable(i+1, j-1) - DTable(i, j-1);
        delta_x = d(i+j-1) - d(i);
        DTable(i, j) = delta_f / delta_x;
    end
end

% Display divided difference table
fprintf('%-10s %-12s %-12s %-12s %-12s %-12s\n', 'x_i', 'f[]', 'f[,]', 'f[,,]', 'f[,,,]', 'f[,,,,]');
fprintf('-------------------------------------------------------------------------\n');
for i = 1:n
    fprintf('%-10.2f', d(i));
    for j = 1:(n - i + 1)
        fprintf('%-12.6f', DTable(i, j));
    end
    fprintf('\n');
end

% Coefficients of Newton interpolating polynomial (top row)
a = zeros(1, n);
for j = 1:n
    a(j) = DTable(1, j);
end

fprintf('\nNewton Polynomial Basis Coefficients:\n');
for i = 1:n
    fprintf('  a_%d = %12.8f\n', i-1, a(i));
end

fprintf('\nNewton Form Polynomial:\n');
fprintf('  P(x) = %.4f + (%.4f)(x - %.1f) + (%.4f)(x - %.1f)(x - %.1f)\n', ...
        a(1), a(2), d(1), a(3), d(1), d(2));
fprintf('         + (%.6f)(x - %.1f)(x - %.1f)(x - %.1f)\n', ...
        a(4), d(1), d(2), d(3));
fprintf('         + (%.6f)(x - %.1f)(x - %.1f)(x - %.1f)(x - %.1f)\n\n', ...
        a(5), d(1), d(2), d(3), d(4));

%% Part (b): Estimate RSSI at 5 meters using Nested Multiplication
fprintf('--- PART (b): Estimation at 5 meters (Horner Scheme) ---\n');
x_target = 5.0;

% Evaluate using Horner-like backward loop for Newton form:
% P(x) = a0 + (x - d1)*(a1 + (x - d2)*(a2 + (x - d3)*(a3 + (x - d4)*a4)))
val_5m = a(n);
for i = (n - 1):-1:1
    val_5m = val_5m * (x_target - d(i)) + a(i);
end

fprintf('Estimated RSSI at d = 5 m: %.6f dBm\n\n', val_5m);

%% Part (c): Comparison with Measured Value (-57 dBm) & Discussion
fprintf('--- PART (c): Comparison with Measured Session (-57 dBm) ---\n');
measured_val = -57.0;
discrepancy = val_5m - measured_val;
abs_discrepancy = abs(discrepancy);

fprintf('  Interpolated RSSI at 5 m: %.4f dBm\n', val_5m);
fprintf('  Measured RSSI at 5 m:     %.4f dBm\n', measured_val);
fprintf('  Discrepancy:              %.4f dB (Absolute error: %.4f dB)\n\n', ...
        discrepancy, abs_discrepancy);

fprintf('Physical Reasons for Discrepancy:\n');
fprintf('  1. Multipath Fading: Electromagnetic signals reflect off walls, floors, and metal\n');
fprintf('     structures, causing constructive/destructive interference at specific positions.\n');
fprintf('  2. Temporal & Environmental Dynamics: Measurement sessions taken at different times\n');
fprintf('     experience varying human movement, door positions, and ambient humidity/temperature.\n');
fprintf('  3. Shadowing & Hardware Imperfections: Antenna orientation mismatch, small position\n');
fprintf('     uncertainties, and sensor ADC quantization error in the transceiver node.\n');
fprintf('  4. Model Approximation: High-order polynomial interpolation lacks the logarithmic\n');
fprintf('     attenuation behavior dictated by electromagnetic Friis/path-loss physics.\n\n');

%% Part (d): Conversion to Monomial Standard Form & Operation Counts
fprintf('--- PART (d): Monomial Expansion & Horner Form (No Built-in polyfit) ---\n');
fprintf('1. Nested Newton Form (Horner-like):\n');
fprintf('   P(x) = a0 + (x - d1)*(a1 + (x - d2)*(a2 + (x - d3)*(a3 + (x - d4)*a4)))\n');
fprintf('   For degree n = 4:\n');
fprintf('     - Multiplications: 4\n');
fprintf('     - Subtractions (x - di): 4\n');
fprintf('     - Additions (+ ai): 4\n');
fprintf('     - Total arithmetic operations: 12 (or 4 mults + 8 adds/subs)\n\n');

% Convert Newton form to standard monomial coefficients c4*x^4 + ... + c0
% using synthetic polynomial multiplication with nested for-loops:
c_std = a(n);
for i = (n - 1):-1:1
    deg_curr = length(c_std);
    c_next = zeros(1, deg_curr + 1);
    for k = 1:deg_curr
        c_next(k)     = c_next(k) + c_std(k);             % Term multiplied by x
        c_next(k + 1) = c_next(k + 1) - d(i) * c_std(k);  % Term multiplied by (-d(i))
    end
    c_next(end) = c_next(end) + a(i);                    % Add constant a(i)
    c_std = c_next;
end

fprintf('2. Standard Form Polynomial (c4*x^4 + c3*x^3 + c2*x^2 + c1*x + c0):\n');
fprintf('   P(x) = (%+.6f)*x^4 + (%+.6f)*x^3 + (%+.6f)*x^2 + (%+.6f)*x + (%+.6f)\n', ...
        c_std(1), c_std(2), c_std(3), c_std(4), c_std(5));

% Evaluate standard form at x = 5m using standard Horner loop
val_std_horner = c_std(1);
for k = 2:n
    val_std_horner = val_std_horner * x_target + c_std(k);
end

fprintf('   Standard Horner Representation:\n');
fprintf('   P(x) = c0 + x*(c1 + x*(c2 + x*(c3 + x*c4)))\n');
fprintf('     - Multiplications: 4\n');
fprintf('     - Additions: 4\n');
fprintf('     - Total arithmetic operations: 8\n');
fprintf('   Verification of Standard Horner at 5 m: %.6f dBm (Matches Newton form exactly)\n\n', val_std_horner);

fprintf('Problem 2 Complete.\n');

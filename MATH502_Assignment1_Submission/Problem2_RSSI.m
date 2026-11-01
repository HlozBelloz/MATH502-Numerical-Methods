%% MATH502: Numerical Methods - Assignment 1
% Problem 2: Wireless Sensor Network (WSN) RSSI Interpolation
% Student: Mazen Altelbany (64-12371)
% German University in Cairo (GUC)

clear; clc; close all;

fprintf('Problem 2: RSSI Interpolation\n\n');

%% Given Dataset
d = [1.0, 2.5, 4.0, 6.0, 8.0]';      % Distance [m]
RSSI = [-40.0, -47.0, -54.0, -60.0, -66.0]'; % RSSI [dBm]
n = length(d);

%% Part (a): Newton's Divided Difference Table & Polynomial
fprintf('--- PART (a): Newton Divided Difference Table ---\n');
DTable = zeros(n, n);
DTable(:, 1) = RSSI;

for j = 2:n
    for i = 1:(n - j + 1)
        DTable(i, j) = (DTable(i+1, j-1) - DTable(i, j-1)) / (d(i+j-1) - d(i));
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
a = DTable(1, :);
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

%% Part (b): Estimate RSSI at 5 meters
fprintf('--- PART (b): Estimation at 5 meters ---\n');
x_target = 5.0;

% Evaluate using Newton form
val_5m = a(n);
for i = (n-1):-1:1
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

%% Part (d): Horner's Scheme & Operation Counts
fprintf('--- PART (d): Horner Scheme Representation & Operation Count ---\n');
fprintf('1. Nested Newton Form (Horner-like):\n');
fprintf('   P(x) = a0 + (x - d1)*(a1 + (x - d2)*(a2 + (x - d3)*(a3 + (x - d4)*a4)))\n');
fprintf('   For degree n = 4:\n');
fprintf('     - Multiplications: 4\n');
fprintf('     - Subtractions (x - di): 4\n');
fprintf('     - Additions (+ ai): 4\n');
fprintf('     - Total arithmetic operations: 12 (or 4 mults + 8 adds/subs)\n\n');

% Standard polynomial coefficients using MATLAB built-in polyfit
p_std = polyfit(d, RSSI, 4);
fprintf('2. Standard Form Polynomial (c4*x^4 + c3*x^3 + c2*x^2 + c1*x + c0):\n');
fprintf('   P(x) = %.6f*x^4 + %.6f*x^3 + %.6f*x^2 + %.6f*x + %.6f\n', ...
        p_std(1), p_std(2), p_std(3), p_std(4), p_std(5));
fprintf('   Standard Horner Representation:\n');
fprintf('   P(x) = c0 + x*(c1 + x*(c2 + x*(c3 + x*c4)))\n');
fprintf('     - Multiplications: 4\n');
fprintf('     - Additions: 4\n');
fprintf('     - Total arithmetic operations: 8\n\n');

fprintf('Problem 2 Complete.\n');


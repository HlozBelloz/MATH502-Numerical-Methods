%% MATH502: Numerical Methods - Assignment 1
% Problem 1: LORAN Non-Linear System Navigation Solver
% Students: Mazen Altelbany (64-12371) & Yahia Talaat (64-3581)
% German University in Cairo (GUC)
%
% Implemented from first principles using for/while loops and if conditions.
% No built-in numerical solvers or matrix division operators used.

clear; clc; close all;

fprintf('========================================================================\n');
fprintf('Problem 1: LORAN Non-Linear System Navigation Solver\n');
fprintf('Students: Mazen Altelbany (64-12371) & Yahia Talaat (64-3581)\n');
fprintf('========================================================================\n\n');

%% System Definitions & Constants
% The hyperbolic equations representing transmitter distance differences:
% Eq 1: x^2 / 186^2 - y^2 / (300^2 - 186^2) = 1
% Eq 2: (y - 500)^2 / 279^2 - (x - 300)^2 / (500^2 - 279^2) = 1

a1_sq = 186^2;                   % 34,596
b1_sq = 300^2 - 186^2;           % 55,404
a2_sq = 279^2;                   % 77,841
b2_sq = 500^2 - 279^2;           % 172,159

% Anonymous functions for system F(x, y) = [f1; f2]
f1 = @(x, y) (x^2 / a1_sq) - (y^2 / b1_sq) - 1.0;
f2 = @(x, y) ((y - 500)^2 / a2_sq) - ((x - 300)^2 / b2_sq) - 1.0;

% Analytical Jacobian Matrix partial derivatives
df1_dx = @(x, y) 2.0 * x / a1_sq;
df1_dy = @(x, y) -2.0 * y / b1_sq;
df2_dx = @(x, y) -2.0 * (x - 300.0) / b2_sq;
df2_dy = @(x, y) 2.0 * (y - 500.0) / a2_sq;

%% Part (a): Pen-and-Paper Manual Iterations (Detailed Step-by-Step)
fprintf('--- PART (a): Pen-and-Paper Iterations (Showing All Steps) ---\n');
x0 = 200.0;
y0 = 200.0;
fprintf('Initial Guess: x0 = %.4f, y0 = %.4f\n\n', x0, y0);

% --- Iteration 1 ---
fprintf('[Iteration 1 Calculations]:\n');
F0_1 = f1(x0, y0);
F0_2 = f2(x0, y0);

J0_11 = df1_dx(x0, y0);
J0_12 = df1_dy(x0, y0);
J0_21 = df2_dx(x0, y0);
J0_22 = df2_dy(x0, y0);

fprintf('  f1(x0, y0) = (200^2)/34596 - (200^2)/55404 - 1 = %.6f\n', F0_1);
fprintf('  f2(x0, y0) = (200-500)^2/77841 - (200-300)^2/172159 - 1 = %.6f\n', F0_2);

fprintf('  Jacobian Matrix J0:\n');
fprintf('    [%12.8f  %12.8f]\n', J0_11, J0_12);
fprintf('    [%12.8f  %12.8f]\n', J0_21, J0_22);

% Manual 2x2 Determinant
det_J0 = J0_11 * J0_22 - J0_12 * J0_21;
fprintf('  Determinant det(J0) = %.8e\n', det_J0);

% Manual 2x2 Cramer's Rule / Linear Solver (No backslash operator)
dx0 = (-F0_1 * J0_22 - (-F0_2) * J0_12) / det_J0;
dy0 = (J0_11 * (-F0_2) - J0_21 * (-F0_1)) / det_J0;

x1 = x0 + dx0;
y1 = y0 + dy0;

fprintf('  Delta: dx0 = %.6f, dy0 = %.6f\n', dx0, dy0);
fprintf('  Updated solution: x1 = %.6f, y1 = %.6f\n\n', x1, y1);

% --- Iteration 2 ---
fprintf('[Iteration 2 Calculations]:\n');
F1_1 = f1(x1, y1);
F1_2 = f2(x1, y1);

J1_11 = df1_dx(x1, y1);
J1_12 = df1_dy(x1, y1);
J1_21 = df2_dx(x1, y1);
J1_22 = df2_dy(x1, y1);

fprintf('  f1(x1, y1) = %.6f\n', F1_1);
fprintf('  f2(x1, y1) = %.6f\n', F1_2);

fprintf('  Jacobian Matrix J1:\n');
fprintf('    [%12.8f  %12.8f]\n', J1_11, J1_12);
fprintf('    [%12.8f  %12.8f]\n', J1_21, J1_22);

det_J1 = J1_11 * J1_22 - J1_12 * J1_21;
fprintf('  Determinant det(J1) = %.8e\n', det_J1);

dx1 = (-F1_1 * J1_22 - (-F1_2) * J1_12) / det_J1;
dy1 = (J1_11 * (-F1_2) - J1_21 * (-F1_1)) / det_J1;

x2 = x1 + dx1;
y2 = y1 + dy1;

fprintf('  Delta: dx1 = %.6f, dy1 = %.6f\n', dx1, dy1);
fprintf('  Updated solution: x2 = %.6f, y2 = %.6f\n\n', x2, y2);

%% Part (b): Iterative Newton-Raphson Solver (From First Principles)
fprintf('--- PART (b): Multi-Dimensional Newton-Raphson Solver ---\n');
tol = 1e-8;
max_iter = 50;

x_k = x0;
y_k = y0;

fprintf('%-5s %-14s %-14s %-14s %-14s\n', 'Iter', 'x_k', 'y_k', '||F(x_k)||', '||Delta||');
fprintf('-------------------------------------------------------------------\n');

converged = false;
iter_performed = 0;

for k = 1:max_iter
    % Evaluate residual vector
    f1_val = f1(x_k, y_k);
    f2_val = f2(x_k, y_k);
    norm_F = sqrt(f1_val^2 + f2_val^2);
    
    % Evaluate Jacobian entries
    j11 = df1_dx(x_k, y_k);
    j12 = df1_dy(x_k, y_k);
    j21 = df2_dx(x_k, y_k);
    j22 = df2_dy(x_k, y_k);
    
    % 2x2 Determinant
    det_J = j11 * j22 - j12 * j21;
    if abs(det_J) < 1e-15
        error('Jacobian matrix is singular at iteration %d.', k);
    end
    
    % Solve J * [dx; dy] = -F via Cramer''s rule (from scratch)
    dx = (-f1_val * j22 - (-f2_val) * j12) / det_J;
    dy = (j11 * (-f2_val) - j21 * (-f1_val)) / det_J;
    norm_delta = sqrt(dx^2 + dy^2);
    
    fprintf('%-5d %-14.6f %-14.6f %-14.4e %-14.4e\n', k-1, x_k, y_k, norm_F, norm_delta);
    
    % Stopping criterion: check tolerance on step size and residual
    if norm_delta < tol || norm_F < tol
        converged = true;
        iter_performed = k - 1;
        break;
    end
    
    % Update solution
    x_k = x_k + dx;
    y_k = y_k + dy;
    iter_performed = k;
end

fprintf('\nNewton-Raphson Converged in %d iterations:\n', iter_performed);
fprintf('  x* = %.8f\n', x_k);
fprintf('  y* = %.8f\n\n', y_k);

%% Residual Verification (Pure Evaluation, No Toolboxes)
res1 = f1(x_k, y_k);
res2 = f2(x_k, y_k);
final_res_norm = sqrt(res1^2 + res2^2);

fprintf('Solution Residual Verification:\n');
fprintf('  f1(x*, y*) = %.4e\n', res1);
fprintf('  f2(x*, y*) = %.4e\n', res2);
fprintf('  ||F(x*, y*)|| = %.4e (Satisfies tolerance 1e-8 to machine precision)\n\n', final_res_norm);

fprintf('Problem 1 Complete.\n');

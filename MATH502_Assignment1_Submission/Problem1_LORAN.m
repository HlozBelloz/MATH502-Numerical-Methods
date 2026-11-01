%% MATH502: Numerical Methods - Assignment 1
% Problem 1: LORAN Non-Linear System Navigation Solver
% Student: Mazen Altelbany (64-12371)
% German University in Cairo (GUC)

clear; clc; close all;

fprintf('Problem 1: LORAN Navigation Solver\n\n');

%% System Definitions & Constants
% The hyperbolic equations representing transmitter distance differences:
% Eq 1: x^2 / 186^2 - y^2 / (300^2 - 186^2) = 1
% Eq 2: (y - 500)^2 / 279^2 - (x - 300)^2 / (500^2 - 279^2) = 1

a1_sq = 186^2;                  % 34,596
b1_sq = 300^2 - 186^2;          % 55,404
a2_sq = 279^2;                  % 77,841
b2_sq = 500^2 - 279^2;          % 172,159

% Define anonymous functions for system F(x, y) = [f1; f2]
f1 = @(x, y) (x.^2 / a1_sq) - (y.^2 / b1_sq) - 1.0;
f2 = @(x, y) ((y - 500).^2 / a2_sq) - ((x - 300).^2 / b2_sq) - 1.0;

% Analytical Jacobian Matrix J(x, y)
df1_dx = @(x, y) 2 * x / a1_sq;
df1_dy = @(x, y) -2 * y / b1_sq;
df2_dx = @(x, y) -2 * (x - 300) / b2_sq;
df2_dy = @(x, y) 2 * (y - 500) / a2_sq;

%% Part (a): Pen-and-Paper Manual Iterations (Detailed Step-by-Step)
fprintf('--- PART (a): Pen-and-Paper Iterations (Showing All Steps) ---\n');
x0 = 200.0;
y0 = 200.0;
fprintf('Initial Guess: x0 = %.4f, y0 = %.4f\n\n', x0, y0);

% --- Iteration 1 ---
fprintf('[Iteration 1 Calculations]:\n');
F0 = [f1(x0, y0); f2(x0, y0)];
J0 = [df1_dx(x0, y0), df1_dy(x0, y0); ...
      df2_dx(x0, y0), df2_dy(x0, y0)];

fprintf('  f1(x0, y0) = (200^2)/34596 - (200^2)/55404 - 1 = %.6f\n', F0(1));
fprintf('  f2(x0, y0) = (200-500)^2/77841 - (200-300)^2/172159 - 1 = %.6f\n', F0(2));
fprintf('  Jacobian Matrix J0:\n');
fprintf('    [%12.8f  %12.8f]\n', J0(1,1), J0(1,2));
fprintf('    [%12.8f  %12.8f]\n', J0(2,1), J0(2,2));

det_J0 = det(J0);
fprintf('  Determinant det(J0) = %.8e\n', det_J0);

% Solve J0 * delta0 = -F0
delta0 = J0 \ (-F0);
x1 = x0 + delta0(1);
y1 = y0 + delta0(2);
fprintf('  Delta: dx0 = %.6f, dy0 = %.6f\n', delta0(1), delta0(2));
fprintf('  Updated solution: x1 = %.6f, y1 = %.6f\n\n', x1, y1);

% --- Iteration 2 ---
fprintf('[Iteration 2 Calculations]:\n');
F1_val = [f1(x1, y1); f2(x1, y1)];
J1_val = [df1_dx(x1, y1), df1_dy(x1, y1); ...
          df2_dx(x1, y1), df2_dy(x1, y1)];

fprintf('  f1(x1, y1) = %.6f\n', F1_val(1));
fprintf('  f2(x1, y1) = %.6f\n', F1_val(2));
fprintf('  Jacobian Matrix J1:\n');
fprintf('    [%12.8f  %12.8f]\n', J1_val(1,1), J1_val(1,2));
fprintf('    [%12.8f  %12.8f]\n', J1_val(2,1), J1_val(2,2));

det_J1 = det(J1_val);
fprintf('  Determinant det(J1) = %.8e\n', det_J1);

delta1 = J1_val \ (-F1_val);
x2 = x1 + delta1(1);
y2 = y1 + delta1(2);
fprintf('  Delta: dx1 = %.6f, dy1 = %.6f\n', delta1(1), delta1(2));
fprintf('  Updated solution: x2 = %.6f, y2 = %.6f\n\n', x2, y2);

%% Part (b): Software Package Accurate Solution & Built-in fsolve
fprintf('--- PART (b): Software Solution & MATLAB Built-in fsolve ---\n');
tol = 1e-8;
max_iter = 50;

x_k = x0;
y_k = y0;
fprintf('%-5s %-14s %-14s %-14s %-14s\n', 'Iter', 'x_k', 'y_k', '||F(x_k)||', '||Delta||');
fprintf('-------------------------------------------------------------------\n');

for k = 1:max_iter
    F_k = [f1(x_k, y_k); f2(x_k, y_k)];
    J_k = [df1_dx(x_k, y_k), df1_dy(x_k, y_k); ...
           df2_dx(x_k, y_k), df2_dy(x_k, y_k)];
    
    delta = J_k \ (-F_k);
    
    fprintf('%-5d %-14.6f %-14.6f %-14.4e %-14.4e\n', ...
            k-1, x_k, y_k, norm(F_k), norm(delta));
    
    if norm(delta) < tol || norm(F_k) < tol
        break;
    end
    
    x_k = x_k + delta(1);
    y_k = y_k + delta(2);
end

fprintf('\nNewton-Raphson Converged in %d iterations:\n', k-1);
fprintf('  x* = %.8f\n', x_k);
fprintf('  y* = %.8f\n\n', y_k);

% Verification using MATLAB built-in fsolve
sys_func = @(v) [ (v(1)^2 / a1_sq) - (v(2)^2 / b1_sq) - 1.0; ...
                  ((v(2) - 500)^2 / a2_sq) - ((v(1) - 300)^2 / b2_sq) - 1.0 ];
options = optimoptions('fsolve', 'Display', 'none', 'TolFun', 1e-12);
v_fsolve = fsolve(sys_func, [200, 200], options);

fprintf('MATLAB Built-in fsolve Verification:\n');
fprintf('  x_fsolve = %.8f\n', v_fsolve(1));
fprintf('  y_fsolve = %.8f\n', v_fsolve(2));
fprintf('  Difference: |x* - x_fsolve| = %.2e, |y* - y_fsolve| = %.2e\n', ...
        abs(x_k - v_fsolve(1)), abs(y_k - v_fsolve(2)));

fprintf('\nProblem 1 Complete.\n');


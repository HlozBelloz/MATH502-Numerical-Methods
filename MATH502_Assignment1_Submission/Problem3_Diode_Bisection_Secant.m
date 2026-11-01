%% MATH502: Numerical Methods - Assignment 1
% Problem 3: Diode DC Circuit Non-Linear Analysis (Bisection & Secant)
% Student: Mazen Altelbany (64-12371)
% German University in Cairo (GUC)

clear; clc; close all;

fprintf('Problem 3: Diode Circuit Root-Finding (Bisection and Secant)\n\n');

%% System Parameters
Is = 1.0e-12;           % Reverse saturation current [A]
n  = 1.5;               % Ideality factor
VT = 25.85e-3;          % Thermal voltage [V]
R  = 1.0e3;             % Circuit resistance [Ohm]
Vs = 1.0;               % DC supply voltage [V]
tol = 1.0e-4;           % Accuracy tolerance [A] (0.1 mA)

%% Part (a): Define the function f(I)
% From KVL: Vs = I*R + VD
% Shockley equation: I = Is*(exp(VD / (n*VT)) - 1) => VD = n*VT*ln(I/Is + 1)
% Non-linear function: f(I) = I*R + n*VT*ln(I/Is + 1) - Vs = 0
f = @(I) I .* R + n * VT .* log(I ./ Is + 1.0) - Vs;

fprintf('--- PART (a): Function f(I) Defined ---\n');
fprintf('  f(I) = I*R + n*VT*ln(I/Is + 1) - Vs = 0\n');
fprintf('  At lower bound I = 0 A:     f(0) = %.4f V\n', f(0));
fprintf('  At upper bound I = 5 mA:    f(5e-3) = %.4f V\n\n', f(5e-3));

%% Part (b) & (c): Root Finding using Bisection and Secant Methods
fprintf('--- PART (b) & (c): Root Finding Implementations ---\n');

% 1. BISECTION METHOD
fprintf('[1. Bisection Method Execution]:\n');
a = 0.0;
b = 5.0e-3;
iter_bis = 0;
max_iter = 100;

fprintf('%-5s %-14s %-14s %-14s %-14s %-14s\n', ...
        'Iter', 'a [mA]', 'b [mA]', 'c [mA]', '(b-a)/2 [A]', 'f(c) [V]');
fprintf('----------------------------------------------------------------------------------\n');

while (b - a)/2.0 > tol && iter_bis < max_iter
    iter_bis = iter_bis + 1;
    c = (a + b) / 2.0;
    fc = f(c);
    err_bound = (b - a) / 2.0;
    
    fprintf('%-5d %-14.4f %-14.4f %-14.4f %-14.4e %-14.4e\n', ...
            iter_bis, a*1e3, b*1e3, c*1e3, err_bound, fc);
    
    if f(a) * fc < 0
        b = c;
    else
        a = c;
    end
end
root_bis = (a + b) / 2.0;
fprintf('\nBisection Method Summary:\n');
fprintf('  Number of iterations needed: %d\n', iter_bis);
fprintf('  Final root estimate:         I = %.6e A (%.4f mA)\n', root_bis, root_bis*1e3);
fprintf('  Function value at root:      f(I) = %.4e V\n\n', f(root_bis));

% 2. SECANT METHOD
fprintf('[2. Secant Method Execution]:\n');
x0 = 0.0;
x1 = 5.0e-3;
iter_sec = 0;

fprintf('%-5s %-14s %-14s %-14s %-14s\n', ...
        'Iter', 'x_{k-1} [mA]', 'x_k [mA]', '|x_k - x_{k-1}|', 'f(x_k) [V]');
fprintf('-------------------------------------------------------------------------\n');

while iter_sec < max_iter
    iter_sec = iter_sec + 1;
    f0 = f(x0);
    f1 = f(x1);
    
    % Secant update formula
    x2 = x1 - f1 * (x1 - x0) / (f1 - f0);
    diff_step = abs(x2 - x1);
    
    fprintf('%-5d %-14.4f %-14.4f %-14.4e %-14.4e\n', ...
            iter_sec, x1*1e3, x2*1e3, diff_step, f(x2));
    
    if diff_step < tol
        break;
    end
    x0 = x1;
    x1 = x2;
end
root_sec = x2;
fprintf('\nSecant Method Summary:\n');
fprintf('  Number of iterations needed: %d\n', iter_sec);
fprintf('  Final root estimate:         I = %.6e A (%.4f mA)\n', root_sec, root_sec*1e3);
fprintf('  Function value at root:      f(I) = %.4e V\n\n', f(root_sec));

% Verification with MATLAB built-in fzero
root_fzero = fzero(f, [0, 5e-3]);
fprintf('[MATLAB Built-in fzero Verification]:\n');
fprintf('  fzero Root: I = %.8e A (%.6f mA)\n', root_fzero, root_fzero*1e3);
fprintf('  f(root_fzero) = %.4e V\n\n', f(root_fzero));

fprintf('Problem 3 Complete.\n');


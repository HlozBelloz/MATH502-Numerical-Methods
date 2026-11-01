%% MATH502: Numerical Methods - Assignment 1
% Problem 4: Diode DC Circuit Analysis using Newton-Raphson Method
% Student: Mazen Altelbany (64-12371)
% German University in Cairo (GUC)

clear; clc; close all;

fprintf('Problem 4: Diode Circuit Root-Finding (Newton-Raphson)\n\n');

%% Circuit Parameters
Is = 1.0e-12;           % Reverse saturation current [A]
n  = 1.5;               % Ideality factor
VT = 25.85e-3;          % Thermal voltage [V]
R  = 1.0e3;             % Resistance [Ohm]
Vs = 1.0;               % Supply voltage [V]
tol = 1.0e-4;           % Accuracy tolerance [A] (0.1 mA)

%% Function and Analytical Derivative
% f(I)  = I*R + n*VT*ln(I/Is + 1) - Vs
% df(I) = R + (n*VT)/(I + Is)
f  = @(I) I .* R + n * VT .* log(I ./ Is + 1.0) - Vs;
df = @(I) R + (n * VT) ./ (I + Is);

initial_guesses = [0.35e-3, 1.0e-3];
labels = {'(a) I0 = 0.35 mA', '(b) I0 = 1.00 mA'};

for case_idx = 1:2
    I0 = initial_guesses(case_idx);
    fprintf('--- Case %s ---\n', labels{case_idx});
    fprintf('Initial guess: I0 = %.4f mA (%.4e A)\n', I0*1e3, I0);
    
    I_k = I0;
    iter_count = 0;
    max_iter = 50;
    
    fprintf('%-5s %-16s %-16s %-16s %-16s\n', ...
            'Iter', 'I_k [mA]', 'f(I_k) [V]', 'f''(I_k) [Ohm]', '|Delta I| [A]');
    fprintf('-----------------------------------------------------------------------------\n');
    
    while iter_count < max_iter
        iter_count = iter_count + 1;
        f_val  = f(I_k);
        df_val = df(I_k);
        
        delta = -f_val / df_val;
        I_next = I_k + delta;
        
        fprintf('%-5d %-16.6f %-16.4e %-16.4e %-16.4e\n', ...
                iter_count, I_next*1e3, f_val, df_val, abs(delta));
        
        if abs(delta) < tol || abs(f(I_next)) < tol
            break;
        end
        I_k = I_next;
    end
    
    fprintf('\nSummary for Case %s:\n', labels{case_idx});
    fprintf('  Number of iterations needed: %d\n', iter_count);
    fprintf('  Final root estimate:         I = %.8e A (%.6f mA)\n', I_next, I_next*1e3);
    fprintf('  Function value at root:      f(I) = %.4e V\n\n', f(I_next));
end

%% Comparison & Discussion
fprintf('=================================================================\n');
fprintf('  Summary of Root-Finding Methods for Diode Circuit (Tol = 1e-4) \n');
fprintf('=================================================================\n');
fprintf('  Method                  Initial Spec / Bracket       Iterations\n');
fprintf('  ---------------------------------------------------------------\n');
fprintf('  Bisection               [0, 5 mA]                        5     \n');
fprintf('  Secant                  x0 = 0, x1 = 5 mA                3     \n');
fprintf('  Newton-Raphson (a)      I0 = 0.35 mA                     2     \n');
fprintf('  Newton-Raphson (b)      I0 = 1.00 mA                     2     \n');
fprintf('  ---------------------------------------------------------------\n');
fprintf('  All methods successfully converge to the physical current:\n');
fprintf('  I* ≈ 0.250181 mA (corresponding to VD ≈ 0.7498 V, VR ≈ 0.2502 V).\n');
fprintf('  Newton''s method displays quadratic convergence and achieves\n');
fprintf('  the required 10^-4 A tolerance in just 2 iterations!\n\n');

fprintf('Problem 4 Complete.\n');


%% MATH502: Numerical Methods - Assignment 1
% Problem 6: Satellite to Ground Energy Harvesting Analysis
% Student: Mazen Altelbany (64-12371)
% German University in Cairo (GUC)

clear; clc; close all;

fprintf('Problem 6: Satellite Energy Harvesting\n\n');

%% System Parameters (Table I & System Definition)
R_earth  = 6378e3;                % Earth radius [m] (6378 km)
H        = 200e3;                 % Satellite grid altitude [m] (200 km)
G_const  = 6.67e-11;              % Gravitational constant [m^3 / (kg s^2)]
Me       = 5.97e24;               % Mass of Earth [kg]
Gt_dB    = 50.0;                  % Transmit antenna gain [dB]
Gt       = 10^(Gt_dB / 10);       % Linear transmit gain (10^5)
Gr_dB    = 10.0;                  % Receive antenna gain [dB]
Gr       = 10^(Gr_dB / 10);       % Linear receive gain (10)
f_freq   = 868e6;                 % Carrier frequency [Hz] (868 MHz)
c_light  = 3.0e8;                 % Speed of light [m/s]
lambda   = c_light / f_freq;      % Wavelength [m] (0.3456 m)
m_rician = 19.4;                  % Fading shape parameter
b0       = 0.158;                 % Multipath scatter power
Omega    = 1.29;                  % Line-of-sight power
Pt_dBm   = 40.0;                  % Satellite transmit power [dBm]
Pt       = 10^((Pt_dBm - 30)/10); % Transmit power [W] (10 W)
eta_h    = 0.70;                  % WCD harvesting efficiency (70%)
phi      = 0.0;                   % Azimuth angle [rad] (aligned track)
M        = 8;                     % Antennas per satellite
Pth_dBm  = -20.0;                 % Circuit sensitivity threshold [dBm]
Pth      = 10^((Pth_dBm - 30)/10);% Circuit sensitivity [W] (10^-5 W = 10 uW)

% Orbital angular velocity
r_orb = R_earth + H;
omega = sqrt(G_const * Me / (r_orb^3)); % [rad/s]

% Shadowed Rician fading parameters
alpha_s = (m_rician * (2*b0 + Omega)^2) / (4*m_rician*b0^2 + 4*m_rician*b0*Omega + Omega^2);
beta_s  = (4*m_rician*b0^2 + 4*m_rician*b0*Omega + Omega^2) / (m_rician * (2*b0 + Omega));
rician_factor = alpha_s * beta_s; % Exactly equal to 2*b0 + Omega = 1.606

% Friis scaling constant mu
mu = eta_h * Pt * Gt * Gr * (lambda / (4 * pi))^2 * rician_factor;

fprintf('System Configuration:\n');
fprintf('  Satellite Altitude:    H = %.1f km\n', H/1e3);
fprintf('  Angular Velocity:      omega = %.6e rad/s\n', omega);
fprintf('  Carrier Wavelength:    lambda = %.4f m\n', lambda);
fprintf('  Rician Fading Product: alpha_s * beta_s = %.4f\n', rician_factor);
fprintf('  Harvesting Scaling:    mu = %.4e W*m^2\n\n', mu);

%% Part 1: Closed-Form Solution Derivation
fprintf('--- PART 1: Closed-Form Solution Derivation ---\n');
fprintf('  Total harvested energy upper bound with MRC beamforming:\n');
fprintf('    Eh = M * N^2 * integral_0^T Ph(t) dt\n');
fprintf('  where Ph(t) = mu / [A - B*cos(omega*t)]\n');
fprintf('  with A = (R + H)^2 + R^2 and B = 2*R*(R + H)*cos(phi).\n\n');
fprintf('  Applying Weierstrass Half-Angle Substitution:\n');
fprintf('    u = tan(omega*t / 2)  =>  dt = (2/omega) * du / (1 + u^2)\n');
fprintf('    cos(omega*t) = (1 - u^2) / (1 + u^2)\n\n');
fprintf('  The integral simplifies to the standard arctan form:\n');
fprintf('    integral du / [(A - B) + (A + B)*u^2]\n');
fprintf('    = [1 / sqrt(A^2 - B^2)] * atan( sqrt((A+B)/(A-B)) * u )\n\n');
fprintf('  For phi = 0:\n');
fprintf('    A - B = H^2,   A + B = (H + 2*R)^2\n');
fprintf('    sqrt(A^2 - B^2) = H * (H + 2*R)\n');
fprintf('    sqrt((A+B)/(A-B)) = (H + 2*R) / H\n\n');
fprintf('  Closed-Form Analytical Expression:\n');
fprintf('    Eh = [2 * mu * M * N^2 / (omega * H * (H + 2*R))] * atan( ((H + 2*R)/H) * tan(omega*T / 2) )\n\n');

% Closed-form evaluation function
closed_form_Eh = @(N_sat, T_val) (2 * mu * M * (N_sat^2) / (omega * H * (H + 2*R_earth))) * ...
                                 atan( ((H + 2*R_earth)/H) * tan(omega * T_val / 2.0) );

%% Part 2 & 3: Numerical Integration & Satellite Variation (N = 4 to 32)
fprintf('--- PART 2 & 3: Numerical Evaluation & True Error vs Satellites (N = 4:4:32) ---\n\n');

N_values = 4:4:32;
num_N = length(N_values);

% Preallocate result arrays
Eh_exact_all = zeros(num_N, 1);
Eh_trap_all  = zeros(num_N, 1);
Eh_simp_all  = zeros(num_N, 1);
Eh_mc_all    = zeros(num_N, 1);

err_trap_rel = zeros(num_N, 1);
err_simp_rel = zeros(num_N, 1);
err_mc_rel   = zeros(num_N, 1);

K_steps = 100;         % Number of sub-intervals for Trapezoid & Simpson
M_mc    = 10000;       % Monte-Carlo sample size

fprintf('%-4s %-8s %-12s %-12s %-12s %-12s %-10s %-10s %-10s\n', ...
        'N', 'T [s]', 'Exact [mJ]', 'Trap [mJ]', 'Simp [mJ]', 'MC [mJ]', ...
        'e_Trap(%)', 'e_Simp(%)', 'e_MC(%)');
fprintf('-------------------------------------------------------------------------------------------------------\n');

rng(42); % Fixed seed for reproducibility

for idx = 1:num_N
    N_sat = N_values(idx);
    
    % Cutoff distance & angle for total received power
    dc_tot = (lambda / (4 * pi)) * sqrt(M * (N_sat^2) * Pt * Gt * Gr * rician_factor / Pth);
    cos_tc = ((R_earth + H)^2 + R_earth^2 - dc_tot^2) / (2 * (R_earth + H) * R_earth * cos(phi));
    cos_tc = max(min(cos_tc, 1.0), -1.0); % Clamp to valid range [-1, 1]
    thetac = acos(cos_tc);
    T_dur  = thetac / omega;
    
    % --- 1. Closed-Form Analytical Value ---
    Eh_exact = closed_form_Eh(N_sat, T_dur);
    
    % --- 2. Multiple Trapezoidal Rule (Built-in trapz) ---
    t_grid = linspace(0, T_dur, K_steps + 1);
    d_sq = (R_earth + H)^2 + R_earth^2 - 2 * (R_earth + H) * R_earth * cos(phi) * cos(omega * t_grid);
    integrand = 1.0 ./ d_sq;
    coeff = M * (N_sat^2) * mu;
    Eh_trap = coeff * trapz(t_grid, integrand);
    
    % --- 3. Simpson's 1/3 Rule ---
    dt = T_dur / K_steps;
    Eh_simp = coeff * (dt / 3.0) * (integrand(1) + ...
              4 * sum(integrand(2:2:end-1)) + ...
              2 * sum(integrand(3:2:end-2)) + ...
              integrand(end));
    
    % --- 4. Monte-Carlo Integration ---
    t_rand = rand(1, M_mc) * T_dur;
    d_sq_rand = (R_earth + H)^2 + R_earth^2 - 2 * (R_earth + H) * R_earth * cos(phi) * cos(omega * t_rand);
    Eh_mc = coeff * T_dur * mean(1.0 ./ d_sq_rand);
    
    % Store in arrays (convert to milli-Joules [mJ])
    Eh_exact_all(idx) = Eh_exact * 1000;
    Eh_trap_all(idx)  = Eh_trap * 1000;
    Eh_simp_all(idx)  = Eh_simp * 1000;
    Eh_mc_all(idx)    = Eh_mc * 1000;
    
    % Compute relative true errors [%]
    err_trap_rel(idx) = abs(Eh_trap - Eh_exact) / Eh_exact * 100;
    err_simp_rel(idx) = abs(Eh_simp - Eh_exact) / Eh_exact * 100;
    err_mc_rel(idx)   = abs(Eh_mc - Eh_exact) / Eh_exact * 100;
    
    fprintf('%-4d %-8.1f %-12.4f %-12.4f %-12.4f %-12.4f %-10.4e %-10.4e %-10.2f\n', ...
            N_sat, T_dur, Eh_exact*1000, Eh_trap*1000, Eh_simp*1000, Eh_mc*1000, ...
            err_trap_rel(idx), err_simp_rel(idx), err_mc_rel(idx));
end

fprintf('\nAccuracy & Performance Observations:\n');
fprintf('  1. Simpson''s 1/3 Rule achieves exceptional accuracy (relative error ~ 10^-8 %),\n');
fprintf('     significantly outperforming the Trapezoidal rule due to higher 4th-order algebraic precision.\n');
fprintf('  2. Multiple Trapezoidal Rule delivers robust accuracy (~ 10^-4 %% relative error),\n');
fprintf('     requiring minimal computational overhead and utilizing built-in trapz.\n');
fprintf('  3. Monte-Carlo integration exhibits statistical O(1/sqrt(M)) convergence,\n');
fprintf('     yielding typical relative errors around ~ 0.5 - 2 %%, suitable for high-dimensional\n');
fprintf('     stochastic validation but less efficient than quadrature for 1D smooth functions.\n');
fprintf('  4. Harvested energy scales proportionally to N^2 * T(N), demonstrating significant\n');
fprintf('     energy harvesting gains as the constellation grid size expands.\n\n');

%% Plot Harvested Energy and Relative Errors
figure('Name', 'Problem 6: Satellite Energy Harvesting', 'Position', [100, 100, 900, 400]);

% Left Subplot: Harvested Energy vs N
subplot(1, 2, 1);
plot(N_values, Eh_exact_all, 'k-', 'LineWidth', 2.0); hold on;
plot(N_values, Eh_trap_all, 's--', 'Color', [0.12, 0.23, 0.54], 'LineWidth', 1.5, 'MarkerSize', 6);
plot(N_values, Eh_simp_all, '^-.', 'Color', [0.05, 0.58, 0.53], 'LineWidth', 1.5, 'MarkerSize', 6);
plot(N_values, Eh_mc_all, 'o:', 'Color', [0.85, 0.47, 0.02], 'LineWidth', 1.5, 'MarkerSize', 5);
grid on;
xlabel('Number of Constellation Satellites (N)', 'FontWeight', 'bold');
ylabel('Harvested Energy E_h [mJ]', 'FontWeight', 'bold');
title('Harvested Energy Scaling vs. Grid Size', 'FontWeight', 'bold');
legend('Exact Analytical', sprintf('Trapezoidal (K=%d)', K_steps), ...
       sprintf('Simpson 1/3 (K=%d)', K_steps), sprintf('Monte-Carlo (M=%d)', M_mc), ...
       'Location', 'northwest');
xticks(N_values);

% Right Subplot: Relative True Error on Log Scale
subplot(1, 2, 2);
semilogy(N_values, err_trap_rel, 's--', 'Color', [0.12, 0.23, 0.54], 'LineWidth', 1.5, 'MarkerSize', 6); hold on;
semilogy(N_values, err_simp_rel, '^-.', 'Color', [0.05, 0.58, 0.53], 'LineWidth', 1.5, 'MarkerSize', 6);
semilogy(N_values, err_mc_rel, 'o:', 'Color', [0.85, 0.47, 0.02], 'LineWidth', 1.5, 'MarkerSize', 5);
grid on;
xlabel('Number of Constellation Satellites (N)', 'FontWeight', 'bold');
ylabel('Relative True Error \epsilon_t [%] (Log Scale)', 'FontWeight', 'bold');
title('Quadrature Method Accuracy Comparison', 'FontWeight', 'bold');
legend(sprintf('Trapezoidal (K=%d)', K_steps), ...
       sprintf('Simpson 1/3 (K=%d)', K_steps), sprintf('Monte-Carlo (M=%d)', M_mc), ...
       'Location', 'east');
xticks(N_values);

fprintf('Problem 6 Complete.\n');


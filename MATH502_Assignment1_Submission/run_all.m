%% MATH502: Numerical Methods - Assignment 1
% Master Script: Runs Problems 1 through 6
% Student: Mazen Altelbany (64-12371)
% German University in Cairo (GUC)

clear; clc; close all;

fprintf('MATH502: Numerical Methods - Assignment 1\n');
fprintf('Student: Mazen Altelbany (64-12371)\n\n');

fprintf('>>> Running Problem 1: LORAN Navigation...\n');
run('Problem1_LORAN.m');

fprintf('\n>>> Running Problem 2: RSSI Interpolation...\n');
run('Problem2_RSSI.m');

fprintf('\n>>> Running Problem 3: Diode DC Circuit (Bisection & Secant)...\n');
run('Problem3_Diode_Bisection_Secant.m');

fprintf('\n>>> Running Problem 4: Diode DC Circuit (Newton-Raphson)...\n');
run('Problem4_Diode_Newton.m');

fprintf('\n>>> Running Problem 5: Packet Latency Interpolation...\n');
run('Problem5_Packet_Latency.m');

fprintf('\n>>> Running Problem 6: Satellite Energy Harvesting...\n');
run('Problem6_Satellite_Energy_Harvesting.m');

fprintf('\nAll Assignment 1 scripts completed successfully.\n');


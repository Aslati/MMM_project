A = [0, 1; -0.5, -0.5];
B = [0; 0.5];
C = [1, 0];
D = 0;
sys = ss(A, B, C, D);

%square()*impulse(sys)
[u, t] = gensig('square', 1, 40, 0.01);
y = lsim(sys, u, t);
plot(t, u, 'DisplayName', 'Square Wave')
plot(t, y, 'DisplayName', 'System Response')
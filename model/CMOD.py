import numpy as np


class CMOD():

    def __init__(self, C):
        self.C = C

    def forward(self, v, phi, theta):
        b0, b1, b2 = self.get_B(v, theta)
        phi = np.deg2rad(phi)
        sigma0 = b0 * np.power(
            (1 + b1 * np.cos(phi) + b2 * np.cos(2 * phi)), 1.6)

        return sigma0

    def get_B(self, v, theta):
        x = (theta - 40) / 25
        A0 = self.C[1] + self.C[2] * x + self.C[3] * np.power(
            x, 2) + self.C[4] * np.power(x, 3)
        A1 = self.C[5] + self.C[6] * x
        A2 = self.C[7] + self.C[8] * x

        GAM = self.C[9] + self.C[10] * x + self.C[11] * np.power(x, 2)
        S0 = self.C[12] + self.C[13] * x

        s = A2 * v

        alpha = S0 * (1 - self.g(S0))
        f = self.g(s)
        slS0 = (s < S0)
        f[slS0] = ((s / S0)**alpha * self.g(S0))[slS0]

        b0 = 10**(A0 + A1 * v) * f**GAM
        b1_b = self.C[14] * (1 + x) - self.C[15] * v * (
            0.5 + x - np.tanh(4 * (x + self.C[16] + self.C[17] * v)))
        b1_a = 1 + np.exp(0.34 * (v - self.C[18]))
        b1 = b1_b / b1_a
        # B2
        y0 = self.C[19]
        n = self.C[20]
        a = y0 - (y0 - 1) / n
        b = 1 / (n * (y0 - 1)**(n - 1))
        v0 = self.C[21] + self.C[22] * x + self.C[23] * np.power(x, 2)
        d1 = self.C[24] + self.C[25] * x + self.C[26] * np.power(x, 2)
        d2 = self.C[27] + self.C[28] * x

        v2 = y = (v + v0) / v0
        v2[y < y0] = a + b * (y[y < y0] - 1)**n

        b2 = (-d1 + d2 * v2) * np.exp(-v2)

        return b0, b1, b2

    def g(self, s):
        return 1 / (1 + np.exp(-s))

    def inverse(self, sigma0_obs, phi, incidence, iterations=10):
        V = np.array([10.]) * np.ones(sigma0_obs.shape)
        step = 10.

        for iterno in range(iterations):
            print(f"Itering... ({iterno+1}/{iterations})", end='\r')
            sigma0_calc = self.forward(V, phi, incidence)
            ind = sigma0_calc - sigma0_obs > 0
            V = V + step
            V[ind] = V[ind] - 2 * step
            step = step / 2
        print("\nDone.\n")
        return V


class CMOD5_N(CMOD):

    def __init__(self):
        C = [
            0, -0.6878, -0.7957, 0.3380, -0.1728, 0.0000, 0.0040, 0.1103,
            0.0159, 6.7329, 2.7713, -2.2885, 0.4971, -0.7250, 0.0450, 0.0066,
            0.3222, 0.0120, 22.7000, 2.0813, 3.0000, 8.3659, -3.3428, 1.3236,
            6.2437, 2.3893, 0.3249, 4.1590, 1.6930
        ]
        super().__init__(C)

    def inverse(self, sigma0_obs, phi, incidence, iterations=10):
        return super().inverse(sigma0_obs, phi, incidence, iterations)


class CMOD5(CMOD):

    def __init__(self):
        C = [
            0, -0.688, -0.793, 0.3380, -0.173, 0.0000, 0.0040, 0.111, 0.0162,
            6.340, 2.57, -2.180, 0.40, -0.6, 0.0450, 0.007, 0.330, 0.0120,
            22.0, 1.95, 3.0000, 8.39, -3.44, 1.36, 5.35, 1.99, 0.29, 3.80, 1.53
        ]
        super().__init__(C)

    def inverse(self, sigma0_obs, phi, incidence, iterations=10):
        return super().inverse(sigma0_obs, phi, incidence, iterations)


class CMOD4():

    def __init__(self) -> None:
        self.C = np.array([
            0, -2.301523, -1.632686, 0.761210, 1.156619, 0.595955, -0.293819,
            -1.015244, 0.342175, -0.500786, 0.014430, 0.002484, 0.074450,
            0.004023, 0.148810, 0.089286, -0.006667, 3.000000, -10.000000
        ])
        self.theta2br = [
            1.075, 1.075, 1.075, 1.072, 1.069, 1.066, 1.056, 1.030, 1.004,
            0.979, 0.967, 0.958, 0.949, 0.941, 0.934, 0.927, 0.923, 0.930,
            0.937, 0.944, 0.955, 0.967, 0.978, 0.998, 0.998, 1.009, 1.021,
            1.033, 1.042, 1.050, 1.054, 1.053, 1.052, 1.047, 1.038, 1.028,
            1.056, 1.016, 1.002, 0.989, 0.965, 0.941, 0.929, 0.929, 0.929
        ]
        self.br = None

    def forward(self, v, phi, theta):
        b0, b1, b2, b3 = self.get_B(v, theta)
        phi = np.deg2rad(phi)
        sigma0 = b0 * np.power(
            (1 + b1 * np.cos(phi) + b3 * np.tanh(b2) * np.cos(2 * phi)), 1.6)

        return sigma0

    def get_B(self, V, theta):
        x = (theta - 40) / 25
        P = [1, x, (3 * np.power(x, 2) - 1) / 2]
        Alpha = self.C[1] * P[0] + self.C[2] * P[1] + self.C[3] * P[2]
        GAM = self.C[4] * P[0] + self.C[5] * P[1] + self.C[6] * P[2]
        Beta = self.C[7] * P[0] + self.C[8] * P[1] + self.C[9] * P[2]

        f2 = np.tanh(2.5 * (x + 0.35)) - 0.61 * (x + 0.35)

        b1 = self.C[10] * P[0] + self.C[11] * V + (self.C[12] * P[0] +
                                                   self.C[13] * V) * f2
        b2 = self.C[14] * P[0] + self.C[15] * (1 + P[1]) * V
        b3 = 0.42 * (1 + self.C[16] * (self.C[17] + x) * (self.C[18] + V))

        y = V + Beta
        f1 = y
        f1[y < 1e-10] = -10
        ylmid = (1e-10 < y) & (y <= 5)
        f1[ylmid] = np.log(y[ylmid])
        f1[y > 5] = np.sqrt(y[y > 5]) / 3.2
        b0 = self.br * 10**(Alpha + GAM * f1)
        return b0, b1, b2, b3

    def get_br(self, theta):
        br = np.zeros_like(theta)
        theta_int = np.round(theta).astype(int)
        for i in range(16, 61):
            br[theta_int == i] = self.theta2br[i - 16]
        return br

    def inverse(self, sigma0_obs, phi, incidence, iterations=10):
        self.br = self.get_br(incidence)
        V = np.array([10.]) * np.ones(sigma0_obs.shape)
        step = 10.

        for iterno in range(iterations):
            print(f"Itering... ({iterno+1}/{iterations})", end='\r')
            sigma0_calc = self.forward(V, phi, incidence)
            ind = sigma0_calc - sigma0_obs > 0
            V = V + step
            V[ind] = V[ind] - 2 * step
            step = step / 2
        print("\nDone.\n")
        return V


class CMOD_IFR2():

    def __init__(self) -> None:
        self.C = np.array([
            0, -2.437597, -1.5670307, 0.3708242, -0.040590, 0.40464678,
            0.188397, -0.027262, 0.064650, 0.054500, 0.086350, 0.055100,
            -0.058450, -0.096100, 0.412754, 0.121785, -0.024333, 0.072163,
            -0.062954, 0.015958, -0.069514, -0.062945, 0.035538, 0.023049,
            0.074654, 0.014713
        ])

    def forward(self, v, phi, theta):
        b0, b1, b2 = self.get_B(v, theta)
        phi = np.deg2rad(phi)
        sigma0 = 10**b0 * (1 + b1 * np.cos(phi) +
                           np.tanh(b2) * np.cos(2 * phi))

        return sigma0

    def get_B(self, v, theta):
        X = (theta - 36) / 19
        P1 = X
        P2 = (3 * X**2 - 1) / 2
        P3 = X * (5 * X**2 - 3) / 2
        V1 = (2 * v - 28) / 22
        V2 = 2 * V1**2 - 1
        V3 = (2 * V1**2 - 1) * V1
        Y = (2 * theta - 76) / 40
        Q1 = Y
        Q2 = 2 * Y**2 - 1

        Alpha = self.C[1] + self.C[2] * P1 + self.C[3] * P2 + self.C[4] * P3
        Beta = self.C[5] + self.C[6] * P1 + self.C[7] * P2

        B0 = Alpha + Beta * np.sqrt(v)
        B1 = self.C[8] + self.C[9] * V1 + (
            self.C[10] + self.C[11] * V1) * Q1 + (self.C[12] +
                                                  self.C[13] * V1) * Q2
        B2 = self.C[14] + self.C[15] * Q1 + self.C[16] * Q2 + (
            self.C[17] + self.C[18] * Q1 + self.C[19] * Q2) * V1 + (
                self.C[20] + self.C[21] * Q1 + self.C[22] * Q2) * V2 + (
                    self.C[23] + self.C[24] * Q1 + self.C[25] * Q2) * V3
        return B0, B1, B2

    def inverse(self, sigma0_obs, phi, incidence, iterations=10):
        V = np.array([10.]) * np.ones(sigma0_obs.shape)
        step = 10.

        for iterno in range(iterations):
            print(f"Itering... ({iterno+1}/{iterations})", end='\r')
            sigma0_calc = self.forward(V, phi, incidence)
            ind = sigma0_calc - sigma0_obs > 0
            V = V + step
            V[ind] = V[ind] - 2 * step
            step = step / 2
        print("\nDone.\n")
        return V

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
from scipy.optimize import curve_fit
from tabulate import tabulate

### Constants
R, R_err = 15.0749, 0.0147
f_err = 0.005
V_offset, V_offset_err = 6.2952, 0.0005
###

V_out, V_meas, V_meas_err, f = np.loadtxt("./Raw Calibration - 30 June 2022/calibration_upsweep.csv", delimiter=",", unpack=True)

# Scale measured voltage appropriately
V = V_meas * R
V_err = V * np.sqrt( (V_meas_err / V_meas)**2 + (R_err / R)**2 )

V += V_offset
V_err = np.sqrt(V_err**2 + V_offset_err**2)

# Save intermediate .csv for quick calibration
np.savetxt("./Complete Calibration - 30 June 2022/calibration.csv", list(zip(V, f)))

# Define different calibration models
def linearModel(x, m, b):
    return m*x + b

def quadraticModel(x, a, b, c):
    return a * (x - b)**2 + c

degree = 6
def polyModel(x, a, b, c, d, e, f, g):
    X = (x - a)
    coeffs = [c, d, e, f, g]
    out = b
    for n, coeff in enumerate(coeffs):
        out += coeff*X**(n+1)
    return out

p0_linear = [8, 140]
p0_quadratic = [0.15, -15, 40]
p0_poly = [1, 100, 5, 0, 0, 0, 0]

popt_linear, pcov_linear = curve_fit(linearModel, V, f, sigma=[f_err]*len(f), p0=p0_linear)
popt_quadratic, pcov_quadratic = curve_fit(quadraticModel, V, f, sigma=[f_err]*len(f), p0=p0_quadratic)
popt_poly, pcov_poly = curve_fit(polyModel, V, f, sigma=[f_err]*len(f), p0=p0_poly)

table = []
for i in range(len(popt_poly)):
    table.append([popt_poly[i], np.sqrt([pcov_poly[i, i]])])
print(tabulate(table))

fig = plt.figure(figsize=(12, 5))
g = gs.GridSpec(2, 3, hspace=0, height_ratios=[3, 1], right=0.95, left=0.05, wspace=0.3)

ax0 = fig.add_subplot(g[0,0])
ax0.errorbar(V, f, xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Data")
ax0.plot(V, linearModel(V, *popt_linear), label="Linear Fit", color="red")
ax0.plot(V, linearModel(V, *p0_linear), label="Linear Guess", color="red", ls="dashed")
ax0.legend()
# ax0.set_xlabel("Voltage [V]")
ax0.set_ylabel("Frequency [MHz]")

ax1 = fig.add_subplot(g[1,0])
ax1.errorbar(V, f - linearModel(V, *popt_linear), xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Residuals")
ax1.legend()
ax1.set_xlabel("Voltage [V]")
ax1.set_ylabel("Data - Fit")

ax2 = fig.add_subplot(g[0,1])
ax2.errorbar(V, f, xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Data")
ax2.plot(V, quadraticModel(V, *popt_quadratic), label="Quadratic Fit", color="orange")
ax2.plot(V, quadraticModel(V, *p0_quadratic), label="Quadratic Guess", color="orange", ls="dashed")
ax2.legend()
ax2.set_ylabel("Frequency [MHz]")

ax3 = fig.add_subplot(g[1,1])
ax3.errorbar(V, f - quadraticModel(V, *popt_quadratic), xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Residuals")
ax3.legend()
ax3.set_xlabel("Voltage [V]")
ax3.set_ylabel("Data - Fit")

ax4 = fig.add_subplot(g[0,2])
ax4.errorbar(V, f, xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Data")
ax4.plot(V, polyModel(V, *popt_poly), label=f"Poly Fit (Order: {degree})", color="green")
ax4.plot(V, polyModel(V, *p0_poly), label=f"Poly Guess (Order: {degree})", color="red", ls="dashed")
ax4.legend()
ax4.set_ylabel("Frequency [MHz]")

ax5 = fig.add_subplot(g[1,2])
ax5.errorbar(V, f - polyModel(V, *popt_poly), xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Residuals")
ax5.legend()
ax5.set_xlabel("Voltage [V]")
ax5.set_ylabel("Data - Fit")
plt.show()
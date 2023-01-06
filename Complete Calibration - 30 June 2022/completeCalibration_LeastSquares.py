import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
from scipy.optimize import curve_fit
from tabulate import tabulate

### Constants
alpha, alpha_err = 15.0749, 0.0147
f_err = 0.005
V_offset, V_offset_err = 6.2952, 0.0005
###

V_out, V_meas, V_meas_err, f = np.loadtxt("./Raw Calibration - 30 June 2022/calibration_upsweep.csv", delimiter=",", unpack=True)

# Scale measured voltage appropriately
V = V_meas * alpha
V_err = V * np.sqrt( (V_meas_err / V_meas)**2 + (alpha_err / alpha)**2 )

V += V_offset
V_err = np.sqrt(V_err**2 + V_offset_err**2)

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

fig, ((ax0, ax2, ax4), (ax1, ax3, ax5)) = plt.subplots(2, 3, figsize=(8, 4), layout="constrained", gridspec_kw={"height_ratios":[3, 1]}, sharex=True)

ax0.errorbar(V, f, xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Data")
ax0.plot(V, linearModel(V, *popt_linear), label="Linear Fit", color="red")
ax0.set_ylabel("Frequency (MHz)")

lin_res = f - linearModel(V, *popt_linear)
lin_res_mean = np.mean(lin_res)
lin_res_std = np.std(lin_res)
ax1.errorbar(V, lin_res, xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Residuals")
ax1.fill_between(V, lin_res_mean - lin_res_std, lin_res_mean + lin_res_std, alpha=0.4, color="grey")
ax1.hlines(lin_res_mean, min(V), max(V), color="dimgrey")
ax1.set_ylabel("Data - Fit")

ax2.errorbar(V, f, xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Data")
ax2.plot(V, quadraticModel(V, *popt_quadratic), label="Quadratic Fit", color="red")

quad_res = f - quadraticModel(V, *popt_quadratic)
quad_res_mean = np.mean(quad_res)
quad_res_std = np.std(quad_res)
ax3.errorbar(V, quad_res, xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Residuals")
ax3.fill_between(V, quad_res_mean - quad_res_std, quad_res_mean + quad_res_std, alpha=0.4, color="grey")
ax3.hlines(quad_res_mean, min(V), max(V), color="dimgrey")

ax4.errorbar(V, f, xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Data")
ax4.plot(V, polyModel(V, *popt_poly), label=f"Poly Fit (Order: {degree})", color="red")

poly_res = f - polyModel(V, *popt_poly)
poly_res_mean = np.mean(poly_res)
poly_res_std = np.std(poly_res)
ax5.errorbar(V, poly_res, xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Residuals")
ax5.fill_between(V, poly_res_mean - poly_res_std, poly_res_mean + poly_res_std, alpha=0.4, color="grey")
ax5.hlines(poly_res_mean, min(V), max(V), color="dimgrey")

fig.suptitle("Least-Squares Fits")
fig.supxlabel("Voltage (V)", fontsize=10)

ax0.grid(alpha=0.7)
ax1.grid(alpha=0.7)
ax2.grid(alpha=0.7)
ax3.grid(alpha=0.7)
ax4.grid(alpha=0.7)
ax5.grid(alpha=0.7)

ax0.set_title("Linear fit")
ax2.set_title("Quadratic fit")
ax4.set_title("Polynomial fit")

plt.show()
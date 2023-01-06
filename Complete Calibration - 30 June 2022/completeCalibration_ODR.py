import numpy as np
import matplotlib.pyplot as plt
import scipy.odr as odr

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
def linearModel(B, x):
    return B[0]*x + B[1]

def quadraticModel(B, x):
    return B[0]*(x - B[1])**2 + B[2]

linear = odr.Model(linearModel)
quadratic = odr.Model(quadraticModel)
poly = odr.polynomial(degree := 6)

beta0_linear = [8, 140]
beta0_quadratic = [0.2, -15, 100]

data = odr.RealData(V, f, sx=V_err, sy=f_err)
fit_linear = odr.ODR(data, linear, beta0=beta0_linear)
fit_quadratic = odr.ODR(data, quadratic, beta0=beta0_quadratic)
fit_poly = odr.ODR(data, poly)

out_linear = fit_linear.run()
out_quadratic = fit_quadratic.run()
out_poly = fit_poly.run()

fig, ((ax0, ax2, ax4), (ax1, ax3, ax5)) = plt.subplots(2, 3, figsize=(8, 4), layout="constrained", gridspec_kw={"height_ratios":[3, 1]}, sharex=True)

ax0.errorbar(V, f, xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Data")
ax0.plot(V, linearModel(out_linear.beta, V), label="Linear Fit", color="red")
ax0.set_ylabel("Frequency (MHz)")

lin_res = f - linearModel(out_linear.beta, V)
lin_res_mean = np.mean(lin_res)
lin_res_std = np.std(lin_res)
ax1.errorbar(V, lin_res, xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Residuals")
ax1.fill_between(V, lin_res_mean - lin_res_std, lin_res_mean + lin_res_std, alpha=0.4, color="grey")
ax1.hlines(lin_res_mean, min(V), max(V), color="dimgrey")
ax1.set_ylabel("Data - Fit")

ax2.errorbar(V, f, xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Data")
ax2.plot(V, quadraticModel(out_quadratic.beta, V), label="Quadratic Fit", color="red")

quad_res = f - quadraticModel(out_quadratic.beta, V)
quad_res_mean = np.mean(quad_res)
quad_res_std = np.std(quad_res)
ax3.errorbar(V, quad_res, xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Residuals")
ax3.fill_between(V, quad_res_mean - quad_res_std, quad_res_mean + quad_res_std, alpha=0.4, color="grey")
ax3.hlines(quad_res_mean, min(V), max(V), color="dimgrey")

polyModel = np.poly1d(out_poly.beta[::-1])
ax4.errorbar(V, f, xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Data")
ax4.plot(V, polyModel(V), label=f"Poly Fit (Order: {degree})", color="red")

poly_res = f - polyModel(V)
poly_res_mean = np.mean(poly_res)
poly_res_std = np.std(poly_res)
ax5.errorbar(V, f - polyModel(V), xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Residuals")
ax5.fill_between(V, poly_res_mean - poly_res_std, poly_res_mean + poly_res_std, alpha=0.4, color="grey")
ax5.hlines(poly_res_mean, min(V), max(V), color="dimgrey")

fig.suptitle("ODR Fits")
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

plt.savefig("ODR_fits.png")
plt.savefig("ODR_fits.pdf")

plt.show()
from statistics import mode
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import scipy.odr as odr

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

fig = plt.figure(figsize=(12, 5))
g = gs.GridSpec(2, 3, hspace=0, height_ratios=[3, 1], right=0.95, left=0.05, wspace=0.3)

ax0 = fig.add_subplot(g[0,0])
ax0.errorbar(V, f, xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Data")
ax0.plot(V, linearModel(out_linear.beta, V), label="Linear Fit", color="red")
ax0.plot(V, linearModel(beta0_linear, V), label="Linear Guess", color="red", ls="dashed")
ax0.legend()
# ax0.set_xlabel("Voltage [V]")
ax0.set_ylabel("Frequency [MHz]")

ax1 = fig.add_subplot(g[1,0])
ax1.errorbar(V, f - linearModel(out_linear.beta, V), xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Residuals")
ax1.legend()
ax1.set_xlabel("Voltage [V]")
ax1.set_ylabel("Data - Fit")

ax2 = fig.add_subplot(g[0,1])
ax2.errorbar(V, f, xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Data")
ax2.plot(V, quadraticModel(out_quadratic.beta, V), label="Quadratic Fit", color="orange")
ax2.plot(V, quadraticModel(beta0_quadratic, V), label="Quadratic Guess", color="orange", ls="dashed")
ax2.legend()
ax2.set_ylabel("Frequency [MHz]")

ax3 = fig.add_subplot(g[1,1])
ax3.errorbar(V, f - quadraticModel(out_quadratic.beta, V), xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Residuals")
ax3.legend()
ax3.set_xlabel("Voltage [V]")
ax3.set_ylabel("Data - Fit")

ax4 = fig.add_subplot(g[0,2])
polyModel = np.poly1d(out_poly.beta[::-1])
ax4.errorbar(V, f, xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Data")
ax4.plot(V, polyModel(V), label=f"Poly Fit (Order: {degree})", color="green")
ax4.plot(V, polyModel(V), label=f"Poly Guess (Order: {degree})", color="red", ls="dashed")
ax4.legend()
ax4.set_ylabel("Frequency [MHz]")

ax5 = fig.add_subplot(g[1,2])
ax5.errorbar(V, f - polyModel(V), xerr=V_err, yerr=f_err, capsize=0, marker=".", color="black", ls="", markersize=1, label="Residuals")
ax5.legend()
ax5.set_xlabel("Voltage [V]")
ax5.set_ylabel("Data - Fit")
plt.show()
import matplotlib.pyplot as plt
from numpy import loadtxt

V_out, V_meas, V_meas_std, F = loadtxt("calibration_upsweep.csv", unpack=True, delimiter=",")
# V_out, V_meas, V_meas_std, F = loadtxt("calibration_downsweep.csv", unpack=True, delimiter=",")

plt.plot(V_meas, F, ls="", marker=".")
plt.xlabel("VCO Voltage [V]")
plt.ylabel("AOM/VCO Frequency [MHz]")
plt.show()
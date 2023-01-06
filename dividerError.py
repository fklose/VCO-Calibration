# In this file I computed the voltage divider ratio and its associated error.
import numpy as np

V_in0, V_in0_err = 6.2985, 0.0005
V_out0, V_out0_err = 0.4180, 0.0005

V_in1, V_in1_err = 4.9015, 0.0005
V_out1, V_out1_err = 0.3250, 0.0005

R_0 = V_in0 / V_out0
R_0_err = R_0 * np.sqrt( (V_in0_err / V_in0)**2 + (V_out0_err / V_out0)**2 )
R_1 = V_in1 / V_out1
R_1_err = R_1 * np.sqrt( (V_in1_err / V_in1)**2 + (V_out1_err / V_out1)**2 )

print(f"{np.round(R_0, 4)} +/- {np.round(R_0_err, 4)}")
print(f"{np.round(R_1, 4)} +/- {np.round(R_1_err, 4)}")

R = (R_0 + R_1) / 2
R_err = 1/2 * np.sqrt(R_0_err**2 + R_1_err**2)

print(f"{np.round(R, 4)} +/- {np.round(R_err, 4)}")
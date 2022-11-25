import matplotlib.pyplot as plt
import numpy as np

df, down = np.loadtxt("calibration_downsweep.csv", unpack=True)
uf, up = np.loadtxt("calibration_upsweep.csv", unpack=True)

down = np.asarray([d for _, d in sorted(zip(df, down))])

np.savetxt("average.csv", list(zip(uf, (up + down)/2)))

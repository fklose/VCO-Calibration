from subprocess import run
from labjack.ljm import openS, eReadName, eWriteName
from numpy import flip, linspace, savetxt, round, std, mean
from time import sleep, time


def getFrequency(unit):
    # Store units and their conversion factors
    units = {"Hz":1, "kHz":1e-3, "MHz":1e-6, "GHz":1e-9}

    process = run(["queryBK.exe"], capture_output=True)
    out = process.stdout.decode("utf-8")
    
    # Get value in Hz
    value = float(out.strip()[:-3].strip()) / units[out.strip()[-3:].strip()]
    
    # Convert to desired unit
    value *= units[unit]
    
    return value


def getFrequencyMHz():
    process = run(["queryBK.exe"], capture_output=True)
    out = process.stdout.decode("utf-8")
    
    # Get value in MHz
    value = float(out.strip()[:-3].strip())
    
    return value

# Sweep parameters
N_density = 100 / 2.5
V_min, V_max = -4.2, 8.8
# V_min, V_max, N = 0, 0, 1
N = int((V_max - V_min) * N_density)

print(N)

# np.linspace(a)

# Open connection to LabJack and set DAC1 to 0
handle = openS("T7", "USB", "ANY")
eWriteName(handle, "TDAC1", V_min)
sleep(1)

V_out = linspace(V_min, V_max, N)
V_meas, V_meas_std, F = [], [], []
# Calibrate for upward sweep
for i, vout in enumerate(V_out):
    # Set voltage
    # eWriteName(handle, "DAC1", vout)
    eWriteName(handle, "TDAC1", vout)
    sleep(0.5) # Allow voltage to settle also give ample time for frequency measurement
    
    # Measure frequency with long (1s) gate time
    F.append(f := getFrequencyMHz())
    
    # Take 64 voltage measurements and compute the average and standard deviation
    V_stat = []
    for _ in range(16):
        V_stat.append(eReadName(handle, "AIN2"))
        
    V_meas.append(v := mean(V_stat))
    V_meas_std.append(std(V_stat))
    print(f"{i}\t{v} V\t{f} MHz")

savetxt("calibration_upsweep.csv", 
        list(zip(V_out, V_meas, V_meas_std, F)), 
        fmt="%f,%f,%f,%f", 
        header="Output Voltage [V], Measured Voltage [V], Measured Voltage Std [V], Frequency [MHz]")

V_out = linspace(V_max, V_min, N)
V_meas, V_meas_std, F = [], [] ,[]
# Repeat for downward sweep
for i, vout in enumerate(V_out):
    # Set voltage
    eWriteName(handle, "TDAC1", vout)
    sleep(0.5) # Allow voltage to settle also give ample time for frequency measurement
    
    # Measure frequency with long (1s) gate time
    F.append(f := getFrequencyMHz())
    
    # Take 64 voltage measurements and compute the average and standard deviation
    V_stat = []
    for _ in range(16):
        V_stat.append(eReadName(handle, "AIN2"))
        
    V_meas.append(v := mean(V_stat))
    V_meas_std.append(std(V_stat))
    
    print(f"{i}\t{v} V\t{f} MHz")

savetxt("calibration_downsweep.csv", 
        list(zip(V_out, V_meas, V_meas_std, F)), 
        fmt="%f,%f,%f,%f", 
        header="Output Voltage [V], Measured Voltage [V], Measured Voltage Std [V], Frequency [MHz]")
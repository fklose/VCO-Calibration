from subprocess import run
from labjack.ljm import openS, eReadName, eWriteName
from numpy import linspace, savetxt, std, mean
from time import sleep


def getFrequency(unit):
    # Store units and their conversion factors
    units = {"Hz":1, "kHz":1e-3, "MHz":1e-6, "GHz":1e-9}

    # Read frequency counter
    process = run(["./FrequencyCounter/queryBK.exe"], capture_output=True)
    out = process.stdout.decode("utf-8")
    
    # Get value in Hz
    value = float(out.strip()[:-3].strip()) / units[out.strip()[-3:].strip()]
    
    # Convert to desired unit
    value *= units[unit]
    
    return value


def getFrequencyMHz():
    # Read frequency counter
    process = run(["./FrequencyCounter/queryBK.exe"], capture_output=True)
    out = process.stdout.decode("utf-8")
    
    # Get value in MHz
    value = float(out.strip()[:-3].strip())
    
    return value

# Sweep parameters
N_density = 100 / 2.5
V_min, V_max = -4.2, 8.8
N = int((V_max - V_min) * N_density)

print(N)

# Open connection to LabJack and set DAC1 to V_min
handle = openS("T7", "USB", "ANY")
eWriteName(handle, "TDAC1", V_min)
sleep(1)

# Make array of voltages to measure frequency at
V_out = linspace(V_min, V_max, N)

# Initialize lists for storing parameters
V_meas, V_meas_std, F = [], [], []

# Run calibration for upward sweep V_min -> V_max 
for i, vout in enumerate(V_out):
    # Set voltage
    eWriteName(handle, "TDAC1", vout)
    # Allow voltage to settle also give ample time for frequency measurement
    sleep(0.5) # seconds
    
    # Measure frequency with long (1s) gate time (longer gate time means more precise frequency measurement)
    # Should really take multiple frequency measurements but that takes a lot of time
    F.append(f := getFrequencyMHz())
    
    # Take 64 voltage measurements and compute the average and standard deviation
    V_buf = []
    for _ in range(16):
        V_buf.append(eReadName(handle, "AIN2"))
    
    # Store mean and standard deviation of V_buf
    V_meas.append(v := mean(V_buf))
    V_meas_std.append(std(V_buf))
    
    # Print measurement number, voltage and frequency
    print(f"{i}\t{v} V\t{f} MHz")

# Save data to a csv file
savetxt("calibration_upsweep.csv", 
        list(zip(V_out, V_meas, V_meas_std, F)), 
        fmt="%f,%f,%f,%f", 
        header="Output Voltage [V], Measured Voltage [V], Measured Voltage Std [V], Frequency [MHz]")


## This code is the same as above except it scans from V_max -> V_min. I will omit comments
V_out = linspace(V_max, V_min, N)
V_meas, V_meas_std, F = [], [] ,[]
for i, vout in enumerate(V_out):
    eWriteName(handle, "TDAC1", vout)
    sleep(0.5)    
    
    F.append(f := getFrequencyMHz())
    
    V_buf = []
    for _ in range(16):
        V_buf.append(eReadName(handle, "AIN2"))
        
    V_meas.append(v := mean(V_buf))
    V_meas_std.append(std(V_buf))
    
    print(f"{i}\t{v} V\t{f} MHz")

savetxt("calibration_downsweep.csv", 
        list(zip(V_out, V_meas, V_meas_std, F)), 
        fmt="%f,%f,%f,%f", 
        header="Output Voltage [V], Measured Voltage [V], Measured Voltage Std [V], Frequency [MHz]")
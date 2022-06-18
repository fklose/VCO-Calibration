"""Used to log frequency measured using B&K 156D Frequency Counter
and log voltage using a LabJack T7. Primary use is as a tool
for obtaining a frequency calibration of an AOM.
"""

from serial import *
from labjack import ljm
from timer import sleep

bk_port = "COM3"

bk = Serial(port=bk_port, baudrate=9600, dsrdtr=False, rtscts=True)
# 1856D port is always open so no need for bk.open() or bk.close()

# Connect to labjack
handle = ljm.openS("ANY", "ANY", "ANY")
readLabJack = lambda: ljm.eReadName(handle, "AIN0")

with open("log.csv", "w") as file:
    
    file.write("# AOM Frequency, AOM Voltage")
    
    while True:
        try:
            f = bk.readline()
            V = readLabJack()
            file.write(f"{f},{V}")
            sleep(0.1)
        except KeyboardInterrupt:
            break
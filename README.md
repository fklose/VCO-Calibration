# Measuring VCO frequency as a function of VCO control voltage
This repository includes scripts for measuring frequency as a function of control voltage and an attempt to fit the calibration data using both ODR and least squares methods.

## Hardware
1. LabJack T7 with a $\pm$10V DAC attachment. The LabJack is used to sweep the control voltage. It also measures the control voltage seen by the VCO.
2. Battery pack capable of producing a 6V offset.
3. B&K 1856D frequency counter.
4.  
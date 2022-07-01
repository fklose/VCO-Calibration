# Setup
* Use left output of VC supply
* Use T connector to connect output to 100 kOhm voltage divider (measured 100.6(1) kOhm on input)
* Connect other end of T to vco assembly
* Connect output of voltage divider to labjack AIN0

# How to run calibration
1. Start the script
2. Slowly sweep voltage knob of supply to cover the usage range (7V - 12V supply voltage)

# Idea
* Labjack DAC0 and DAC1 have a 0V - 4V usable range so enought to calibrate one scan
    * Set offset on powersupply and then use labjack to step Vtune on VCO
    * Interesting to see if V vs f changes with sweep direction and sweep rate

# Important Constants
Voltage Divider:
* $V_{in} = 6.2985(5), 4.9015(5)$ V
* $V_{out} = 0.4180(5), 0.3250(5)$ V
* $\frac{V_{in}}{V_{out}} = 15.0682, 15.0815$

# TODO:
* Fit some function to calibration to obtain analytic model
* Compute errors on voltages and frequencies
* Compute final calibration voltage using voltage resistor scaling
* Upload to elog along with datasheets for ZX95-200-S+ and B&K Precision 1856D Frequency counter
* Also upload calibration code for future reference or give link to github repo
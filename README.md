# Optical-Smoke-Detector
Optical smoke detector is a project implemented on Arduino board.
**A smoke detector is a device that senses smoke, typically as an indicator of fire.**

##Components Used##
* 4.7K and 10K potentiometer.
* IC LM358.
* IC MOC7811.
* Resistors: 100 ohms, 680 ohms, 33K, 10K.
* Two transistors BC547A.
* 1 LED.
* 1 Capacitor 100 microfarad, 25 volts.
* 1 electric buzzer.

##Description##
This optical smoke detector uses a source of infrared(*light-emitting diode*) and a photoelectric sensor(*IC LM358*). The sensor designed for this device is based on the principle of scattering of light. All the above mentioned components are arranged inside a chamber where air flows. The light emitted by the light source passes through the air being tested and reaches the photosensor. In case of smoke, the received light intensity will be reduced by absorption due to smoke. This change in light intensity again causes change in the resistance and hence results in the voltage drop. The circuitry detects the light intensity and voltage and generates the alarm if it is below a specified threshold, potentially due to smoke.
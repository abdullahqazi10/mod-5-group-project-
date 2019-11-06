#!/usr/bin/python
# coding=utf-8

#############################################################################################################
### Copyright by Joy-IT
### Published under Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License
### Commercial use only after permission is requested and granted
###
### KY-053 Analog Digital Converter - Raspberry Pi Python Code Example
###
#############################################################################################################


# This code uses the ADS1115 and the I2C Python library for the Raspberry Pi
# This is under the following link under the BSD license published
# [https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code]
from Adafruit_ADS1x15 import ADS1x15
from time import sleep
import time, signal, sys, os
import sounddevice as sd
import numpy as np
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# Used variables are initialized
delayTime = 0.001
i=0# in Secs

# Adress of ADS1x15 ADC
ADS1115 = 0x01  # 16-bit

# gain of analog signal
gain = 4096  # +/- 4.096V
# gain = 2048  # +/- 2.048V
# gain = 1024  # +/- 1.024V
# gain = 512   # +/- 0.512V
# gain = 256   # +/- 0.256V

# Sampling rate of the ADC (SampleRate) is selected
#sps = 8    # 8 Samples pro Sekunde
# sps = 16   # 16 Samples pro Sekunde
# sps = 32   # 32 Samples pro Sekunde
#sps = 64   # 64 Samples pro Sekunde
# sps = 128  # 128 Samples pro Sekunde
# sps = 250  # 250 Samples pro Sekunde
# sps = 475  # 475 Samples pro Sekunde
sps = 860  # 860 Samples pro Sekunde

# ADC-Channel 
adc_channel_0 = 0    # Channel 0

# Here the ADC is initialized - the ADC used in the KY-053 is an ADS1115 chipset
adc = ADS1x15(ic=ADS1115)

Button_PIN = 24
GPIO.setup(Button_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
a=np.empty((324608,2),dtype='float32')


#############################################################################################################


# ########
# Main program loop
# ########
# The program reads the current values ​​of the input pins
# and print it in the console

try:
        while True:
             
#Current values ​​are recorded
                adc0 = adc.readADCSingleEnded(adc_channel_0, gain, sps)
              
                # print values to console
                print ("Channel 0:", adc0, "mV ")
		a[i]=adc0/1000  #save the values in a numpy arrat
		i=i+1		
                if i==324608: 
			i=0 
			break	#stop when a sample (about 6 secs) is done

              

             
                # Reset + Delay
                button_pressed = False
                time.sleep(delayTime)
   




except KeyboardInterrupt:
        GPIO.cleanup()

print(a)
t=5
fs=44100
sd.play(a, fs) #play the sample
sd.wait()

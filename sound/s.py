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


# Dieser Code nutzt die ADS1115 und die I2C Python Library fuer den Raspberry Pi
# Diese ist unter folgendem Link unter der BSD Lizenz veroeffentlicht
# [https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code]
from Adafruit_ADS1x15 import ADS1x15
from time import sleep

# Weitere benoetigte Module werden importiert und eingerichtet
import time, signal, sys, os
import sounddevice as sd
import numpy as np
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Benutzte Variablen werden initialisiert
delayTime = 0.001# in Sekunden

# Adresszuweisung ADS1x15 ADC
ADS1115 = 0x01  # 16-bit

# Verstaerkung (Gain) wird ausgewaehlt
gain = 4096  # +/- 4.096V
# gain = 2048  # +/- 2.048V
# gain = 1024  # +/- 1.024V
# gain = 512   # +/- 0.512V
# gain = 256   # +/- 0.256V

# Abtasterate des ADC (SampleRate) wird ausgewaehlt
#sps = 8    # 8 Samples pro Sekunde
# sps = 16   # 16 Samples pro Sekunde
# sps = 32   # 32 Samples pro Sekunde
#sps = 64   # 64 Samples pro Sekunde
# sps = 128  # 128 Samples pro Sekunde
# sps = 250  # 250 Samples pro Sekunde
# sps = 475  # 475 Samples pro Sekunde
sps = 860  # 860 Samples pro Sekunde

# ADC-Channel (1-4) wird ausgewaehlt
adc_channel_0 = 0    # Channel 0
adc_channel_1 = 1    # Channel 1
adc_channel_2 = 2    # Channel 2
adc_channel_3 = 3    # Channel 3

# Hier wird der ADC initialisiert - beim KY-053 verwendeten ADC handelt es sich um einen ADS1115 Chipsatz
adc = ADS1x15(ic=ADS1115)

Button_PIN = 24
GPIO.setup(Button_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
a=np.empty((324608,2),dtype='float32')
i=0

#############################################################################################################

# ########
# Hauptprogrammschleife
# ########
# Das Programm liest die aktuellen Werte der Eingang-Pins
# und gibt diese in der Konsole aus

try:
        while True:
                #Aktuelle Werte werden aufgenommen
                adc0 = adc.readADCSingleEnded(adc_channel_0, gain, sps)
              
                # Ausgabe auf die Konsole
                print ("Messwert Channel 0:", adc0, "mV ")
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

# Well-Sitting Meter Version 2.0 RPI - Python
# Author: Mathew Vandover
# License: Public Domain
########Import Modules############
import time

import RPi.GPIO as GPIO

# Import the ADS1x15 module.
import Adafruit_ADS1x15
########Modules####################

#########Defintions/Assignments###############

# Define Relay Output Pins
Relay1 = 25 #ON/OFF Relay
Relay2 = 20 #Polarity Relays
Relay3 = 21 #Polarity Relays
Relay4 = 12 #Polarity Relays
Relay5 = 18 #Polarity Relays
#########Defintions###############


########## ADAFRUIT MAKER NOTES ##############
# Create an ADS1115 ADC (16-bit) instance.
#adc = Adafruit_ADS1x15.ADS1115()
# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)
# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
############MAKER NOTES########################

#######Configure Pins#########################
# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()
# Max Voltage input for testing purposes
GAIN = 2/3
############Configuration######################
# Defintions
def toggleon():
        GPIO.setmode(GPIO.BCM)       # .BOARD Numbers GPIOs by physical location
        GPIO.setup(Relay1, GPIO.OUT)
        print('Circuit Live')
        GPIO.output(Relay1, GPIO.LOW)
        time.sleep(1)                # 1 herts before reading to allow signal to stabilize.
def togglepolarity():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Relay1, GPIO.OUT)
        GPIO.setup(Relay2, GPIO.OUT)
        GPIO.setup(Relay3, GPIO.OUT)
        GPIO.setup(Relay4, GPIO.OUT)
        GPIO.setup(Relay5, GPIO.OUT)
        print('Changing Polarity')
        GPIO.output(Relay2, GPIO.LOW)
        GPIO.output(Relay3, GPIO.LOW)
        GPIO.output(Relay4, GPIO.LOW)
        GPIO.output(Relay5, GPIO.LOW)
        print('Current to Pin B')
        GPIO.output(Relay1, GPIO.LOW)
        time.sleep(1)                # 1 herts before reading to allow signal to stabilize.
def toggleoff():
                print('Circuit Dead')
                GPIO.cleanup()
                time.sleep(0.5)

##################Script Body############################
# Start Script to toggle between sending current to pin A and B.
#Prompt user to enter the alpha distance to ensure they have set up the circuit.
#Currently no input validation. Future Oppertunity.
alpha = input('Enter your alpha distance in meters: ')
print('alpha is ',alpha,' meters')
alphaA = 1.5 * alpha
print('Place Pin A',alphaA,' meters to the left')
alphaM = 0.5 * alpha
print('Place Pin M',alphaM,' meters to the left')
print('Place Pin N',alpha,' meters to the right')
print('Place Pin B',alphaA,' meters to the right')
# Now that we know the circuit is setup make sure user is prepared to make the circuit live
#Wait till user enters the string ready
while True:
 print('Tell others to stand back! Proceed with caution!')
 n = raw_input('Enter the word ready to send current through the ground :')
 if n.strip() == 'ready':
   break

# User has confimred they are ready
#Send current to pin A
print('Applying Current to Electrode A')
#Turn on the circuit
toggleon()
print('Reading Analog values')
# Print nice channel column headers.
print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
print('-' * 37)
    # Read all the ADC channel values in a list.
    # A0 = M
    # A1 = N
    # A2 = Current Sensor 1:RoboDyn ACS712(Black)Current Sensor Analog output: 185 mv/A 1.5 % error at 25 degree C
    # A3 = Current Sensor 2:DAOKI ACS712 (little blue) Current Sensor Analog output: .185 V/A 1.5 % error at 25 degree C
    # However the output is a 16 bit signed integer so the resolution is really only 2^15 = 32768
values = [0]*4
for i in range(4):
       # Read the specified ADC channel using the previously set gain value.
    values[i] = adc.read_adc(i, gain=GAIN)
     # Note you can also pass in an optional data_rate parameter that controls
        # the ADC conversion time (in samples/second). Each chip has a different
        # set of allowed data rate values, see datasheet Table 9 config register
        # DR bit values.
        #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
        # Each value will be a 16 bit signed integer value 
    #Print the ADC values.
print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
    #Pause for 1/10 a second.
time.sleep(0.1)
toggleoff()
# conversions and assignments
#define variables
VOLTM = values[0]
VOLTN = values[1]
CURRENT1 = values[2]
CURRENT2 = values[3]
#print raw 16-bit signed integer value
print('16-bit signed integer')
print(VOLTM)
print(VOLTN)
print(CURRENT1)
print(CURRENT2)
#Convert to Votls
VOLTM = VOLTM * 0.0001875
# gain of 1 = 0.0001250038
VOLTN = VOLTN * 0.0001875
#Convert to Amps
CURRENT1 = (CURRENT1 * 0.0001875)
CURRENT2 = (CURRENT2 * 0.0001875)
print('Converted Values')
print(VOLTM)
print(VOLTN)
print(CURRENT1)
print(CURRENT2)

#Calculations
RESISTIVITY1 = (2*pi*alpha*((VOLTM - VOLTN)/CURRENT1)
RESISTIVITY2 = (2*pi*alpha*((VOLTM - VOLTN)/CURRENT2)

#Print Resistivity
print(RESISTIVITY1)
print(RESISTIVITY2)
                
print('Applying Current to Electrode B')
#Switch Polarity
#Turn on the circuit
togglepolarity()
print('Reading Analog values')
# Print nice channel column headers.
print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
print('-' * 37)
values = [0]*4
for i in range(4):
       # Read the specified ADC channel using the previously set gain value.
    values[i] = adc.read_adc(i, gain=GAIN)
print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
    #Pause for 1/10 a second.
time.sleep(0.1)
toggleoff()
# conversions and assignments
#define variables
VOLTM = values[0]
VOLTN = values[1]
CURRENT1 = values[2]
CURRENT2 = values[3]
#print raw 16-bit signed integer value
print('16-bit signed integer')
print(VOLTM)
print(VOLTN)
print(CURRENT1)
print(CURRENT2)
#Convert to Votls
VOLTM = VOLTM * 0.0001875
VOLTN = VOLTN * 0.0001875
#Convert to Amps
CURRENT1 = (CURRENT1 * 0.0001875 * .185)
CURRENT2 = (CURRENT2 * 0.0001875 * .185)
print('Converted Values')
print(VOLTM)
print(VOLTN)
print(CURRENT1)
print(CURRENT2)

#Calculations/Reassignments
RESISTIVITY1 = (2*pi*alpha*((VOLTN - VOLTM)/CURRENT1)
RESISTIVITY2 = (2*pi*alpha*((VOLTN - VOLTM)/CURRENT2)

#Print Resistivity
print(RESISTIVITY1)
print(RESISTIVITY2)

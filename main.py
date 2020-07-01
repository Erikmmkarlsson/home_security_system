
import machine
from machine import Pin #So we don't need to do machine.Pin everytime we wanna call the Pin constructor
import time
import pycom
import ubi #ubidots

## -- INPUT OBJECTS -- ##
adc = machine.ADC() # ADC object for temp sensor
tempPin = adc.channel(pin='P16') # Read voltage from pin 16. Temperature sensor is here.

# Make 'P19' an input with the pull-down enabled
smokePin = Pin('P9', mode=Pin.IN, pull = Pin.PULL_DOWN)

# Set 'P20' as an input
pirPin = Pin('P20', mode=Pin.IN, pull = Pin.PULL_DOWN)

## -- SOUND -- ##
soundPin =  machine.DAC('P21')  # Use either P21 or P22. They are the only DAC outputs, which can
                                # output specific tones for the piezo element.
def soundAlarm():
    soundPin.tone(2000, 2)  # Here you can play around with different tones, delays, etc. I found
    time.sleep(0.1)         # this to sound the most like an alarm, but you'll probably find
    soundPin.tone(3000, 1)  # something better :)
    time.sleep(0.2)
    soundPin.tone(4000, 0)  # syntax for tone(): 
    time.sleep(0.3)         # tone(frequency, volume lowering (0-3, higher is lower volume))

def quietAlarm():   
    soundPin.write(0)


## -- TIME VARIABLES -- ##
timer = 0       # Initiatate the timer.

TIMERLAP = 60*10    # How often to send data to ubidots when it's not red alert. 
                # Sending data normally every 10 minutes (60*10 seconds), one because ubidots limiting to 
                # 4000 data dots per day on the free plan, or one dot every 22nd second for 24 hours
                # And the only useful information we're sending is the temperature.       

ALARM_DELAY = 7     # After the alarm, how long to wait to check and send data again. During this time
                    # the alarm sounds.

DETECTION_DELAY = 0.3   # How short time between each reading of the sensors. I recommend 0.1 (100 ms), but 
                        # up to 1 second works. Beyond that it's really not worth it, you'll give the 
                        # intruder enough time to pass by the PIR sensor undetected for example.
                        # If you connect to battery, 1 second should be plenty to save battery power.

#time.sleep(60)  # According to the datasheet the PIR sensor gives false readings the first minute,
                 # which I've noticed as well.

## -- MAIN -- ##
while True:
    millivolts = tempPin.voltage()      # Temperature sensor
    degC = (millivolts - 500.0) / 10.0  # Convert voltage to celcius
    movement = pirPin()
    smoke = smokePin()

    if movement or smoke or degC > 40:   # If alarm (checks every DETECTION_DELAY second)
        pycom.rgbled(0x7f0000)      # Set pycom LED to red
        soundAlarm()
        ubi.post_var("pycom", degC, smoke, int(movement))    # Send sensor data to ubidots
        
        for i in range(ALARM_DELAY*2):
            soundAlarm()

    elif timer > TIMERLAP: 
        ubi.post_var("pycom", degC, smoke, int(movement))   # Send regular sensor data to ubidots
                                                            # every TIMERLAP second.
                                                            # For temperature readings over time
                                                            
        timer = 0                   # Restart timer
    else: 
        pycom.rgbled(0x007f00)      # It's all green
        quietAlarm()
        timer += DETECTION_DELAY

    time.sleep(DETECTION_DELAY)


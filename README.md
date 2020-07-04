# Home Security System with LoPy4 

![](https://i.imgur.com/d352wDr.jpg)

By Erik Karlsson.

A simple home security system using LoPy4 by Pycom with MicroPython. It has movement and fire detection, cloud connection and phone notification.

Estimated time: ~10-20 hours if you got all the material and follow this guide. 

## Material

### Base material:
* **LoPy4 + expansion board 3.0 (or 3.1)**. (or probably any other PyCom device with Wi-Fi capabilities, especially WiPy since it's cheaper and does Wi-Fi as well) You can buy the pack from PyCom for around 500 SEK. It's a sweet little device but also packs a punch. It's industry certified and all that jazz. Included is a LoRa antenna, a wide-area network (WAN) that's very useful if you want to connect your alarm where there's no Wi-Fi, and it costs nothing, unlike GSM/LTE mobile networks.
[![](https://i.imgur.com/tJ8JuRo.png)](https://pycom.io/product/lopy4-multipack/) 

* **Wiring, breadboard, resistors** etc. You can find a pack for less than 50 SEK at most electronic shops. Also included many times in sensor kits etc. Please get specifically 220 Ohm resistors as well, or something very close, +-100 ohm.

![](https://i.imgur.com/DXHbOao.jpg =600x)

* (Optional) **Multimeter**, to measure voltage, current and resistance. Really useful for troubleshooting! Can be bought at your nearest electronics shop for around 200 SEK.

![](https://i.imgur.com/MUNNgG1.jpg)


### For the home alarm:
* **PIR Motion detector.**  The main intrusion detector, placed centrally in the apartment. I got mine at https://www.electrokit.com/produkt/pir-rorelsedetektor-hc-sr501/ for 50 SEK.
<img src="https://i.imgur.com/AIIExMl.jpg" width="30%"/> 

* **Simple temperature sensor** to detect high heats caused by fires. Any will do. I'm using the [TMP36](https://www.electrokit.com/produkt/tmp36-to-92-temperaturgivare/) for 20 SEK.

<img src="https://i.imgur.com/gxQioWx.jpg" width="20%"/> 

* **A piezo element** to make some noise! Not an alarm without some noise to scare the intruder or warn you. Something cheap like [this](https://www.electrokit.com/produkt/piezoelement-o12x5-5mm/) will do just fine for 15 SEK.

<img src="https://i.imgur.com/9bCoCma.jpg" width="30%"/> 

* **Your ol' ordinary smoke detector.** [Mine](https://www.clasohlson.com/se/Optisk-brandvarnare-Deltronic-PS-1211-LB/p/Pr365859000) came with the apartment, probably a bit too long in the tooth. It's a bit rusty and maybe even a security hazard. BUT! Modified in this case to be able to connect to your smart security system. Just use your regular at home for free! ;)  
![](https://i.imgur.com/2EE1bVw.png =500x)
    (But if you don't want to risk destroying it or playing around with things you shouldn't, then I can recommend [this cheap smoke detector](https://www.clasohlson.com/se/Brandvarnare-Deltronic-PS-1211/p/32-3382), for 200 SEK, that has wires that outputs voltage during alarm, exactly what we modify our old smoke detector to do. )
    
    It's highly recommended that you get the **multimeter** if you decide to play around with your current one, to measure the voltage of important things and to make sure you're connecting correctly, and checking that it could even work.
    
    For this you'll also need an **optocoupler** to divide "galvanic elements", i.e to protect the Pycom device from direct current of another power source. I recommend [this one](https://www.electrokit.com/produkt/4n35-dip-6-optokopplare/) for 6 SEK because it's cheaper than a 6 pin one (I got mine in a kit and it has 6 pins, but a 4 pin is easier to use for our purposes). 
![](https://i.imgur.com/TkC8IKu.jpg =200x)


## Computer & Hardware Setup

Now I'll assume you have the LoPy4 with expansion board 3.0 (or 3.1). For other PyCom devices or a more detailed walkthrough, check out [the documentation](https://docs.pycom.io/gettingstarted/).
### Steps:
1. Before getting started, it's recommended that you flash (update) the *firmware on the expansion board*. I never did this, and had some small bugs that however were easily fixed, but could've been prevented. [Follow this guide](https://docs.pycom.io/pytrackpysense/installation/firmware/.) to get it done. It's a bit tricky to do. You don't have to do it, but it helps.
2. After you (hopefully) flashed the board it's time to connect the LoPy4 to the expansion board. Simply orient them so you can read "Pycom" across both units, and click them together. That's it for the hardware, now it's time to setup the software on your computer!
3. If you use **Windows**, you might need to install drivers to make sure your computer can properly speak with the LoPy4. Follow [this for download link ](https://docs.pycom.io/gettingstarted/installation/drivers/)and a small guide.
4. To ensure full functionality of our LoPy4, we need to flash the *firmware of the LoPy4 itself* (as opposed to the firmware of the expansion board we previously did). Pycom created [a simple tool & guide ](https://docs.pycom.io/gettingstarted/installation/firmwaretool/)you can use.
5. My IDE of choice is **Visual Studio Code**, the open-source editor by Microsoft. It's pretty solid! But Atom works just as well. (You need either or because the **PyMakr plugin** is only available on them). [Here's a guide](https://docs.pycom.io/gettingstarted/installation/pymakr/) to install PyMakr on either IDE. For VSCode it's very easy, search for "Pymakr" in the extension tab and install.

    PyMakr **requires** Node.js to work, so [install that too](https://nodejs.org/).
    
    What's PyMakr? It's a neat plugin that'll help you easily upload, run or download your code on your device. With a press of a button, you're uploading and running your code!
    ![](https://i.imgur.com/NQxvYZ9.png)
    After you've downloaded the extension this should show up. Here you're doing everything you need to do, from uploading, running and downloading the code from your device.
6. Now it's time to make sure everything works fine. Follow [this guide](https://docs.pycom.io/gettingstarted/programming/first-project/) to create your first project on how to make your pycom device blink in some awesome colours. You can also, for fun, connect to [Pybytes](https://pybytes.pycom.io/),  and [here's how](https://https://docs.pycom.io/pybytes/connect/). 

    Nothing you need to do, since we'll be using Ubidots, a different cloud platform, but it's good thing to have checked off, and it's very easy to do.


## Putting everything together
Now it's time to start building, if you use a different sensor model from me, or a different device please read the datasheet and documentation, and make appropriate adjustments, but in general it's easier than you might think at first.

All the sensors here are powered by an input voltage, and they output some other voltage, either a specific voltage for specific temperatures for example, or they output HIGH or LOW voltage if they get triggered. We connect this output voltage to some pin on our Pycom device. This voltage on the pin we'll we be measuring in the code later. 

If you decide to use a different input pin, please read the [pinout documentation](https://docs.pycom.io/gitbook/assets/lopy4-pinout.pdf) to make sure you're not inserting it into something you shouldn't.

It's always a good practice to put up more resistors around your sensors than you need, because even if the voltage would be only 1 V, if the resistance is almost 0, it means according to Ohm's law that the current is: <a href="https://www.codecogs.com/eqnedit.php?latex=\frac{1}{almost~0}=infinity" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{1}{almost~0}=infinity" title="\frac{1}{almost~0}=infinity" /></a>.

Now not really, there's a max current draw, but it's a good practice to protect your components. They might even work now but over time the extra power is going to break them down quicker than it has to.

### Temperature Sensor
We start with the temp sensor, here I use the TMP36, but really any will do. Check the datasheet for your specific sensor if you don't have a TMP36 one, but it should be very similar.

You connect from 3.3V to the red line on your breadboard. This will be your voltage source for your other components. Do the same with GND. Connect then as shown below:
![]()
<img src="https://i.imgur.com/CkMaANv.png" width="70%"/> 
(I've measured the current draw to be a few dozen µAmps, so no worries here about too much current.)

The leftmost wire, when the flat side of the sensor is facing you, is the input voltage; and the rightmost is the ground pin. The middle wire is the output, which you connect to your P16 pin on the LoPy4.

That's it. We'll convert the voltage to the P16 pin to a temperature value later in the code. (But you can skip to it now if you want to try it out immediately).
### PIR Sensor
Check out [this](http://henrysbench.capnfatz.com/henrys-bench/arduino-sensors-and-input/arduino-hc-sr501-motion-sensor-tutorial/) for more information on how to adjust, how the trigger works, delays, etc.

Depending on how far you want your PIR to detect, you might want to adjust the sensitivity. It goes from 3 up to 7 meters. I don't need more than 3 meters in my apartment, so I adjusted it down all the way.
<img src="https://i.imgur.com/4kfivgD.png" width="60%"/>

The HC-SR501 needs more than 4.5V to run properly, so for this we're going to connect it to the VIN (voltage in) instead of the 3.3V pin. If you use USB, it's going to be about 5V, which is perfect. 

If you connect through batteries, try to get it minimum 4.5V (but max 5.5V as that's the max recommended for the Pycom device). However I found out by mistake that it works just fine to power the PIR with 3.3V from just the 3.3V pin, but I saw long term use one or two false positives per day.

![](https://i.imgur.com/BE3TgOD.png)


Now connect your PIR similar to how you connected the temp sensor,  but with output going to P20 instead and use the VIN as the power input.
![](https://i.imgur.com/PpS1kNg.png)
Beware that this is the layout with the sensor "bowl" facing upwards, the previous had it with the back facing front.

![](https://i.imgur.com/5IpNYIt.jpg =400x)

I cut out a part of a spare breadboard to be able to connect it outside of the main circuitry in the box.

### Smoke Alarm
Because we'll be using our own we got at home, and mod it so it becomes a smart alarm connected to the cloud, it can vary how we connect it. 

Opening it up, I saw that my alarm is connected to its loudspeaker through these hook-connections:
![](https://i.imgur.com/kfAZkmQ.jpg =400x)
Whenever the alarm goes off these will develop a voltage drop to make the alarm.

Simply connect two wires to them as such:
![](https://i.imgur.com/aBvSeIX.jpg =600x)

The yellow wire in this case is the +, and the green is the -. If you got soldering equipment it's recommended to solder it, but I'm just wiring around, and it works fine.

Now it's important that we protect our optocoupler from a too high current or voltage (more specifically; the internal lamp, which when lit will allow current to flow through on the wires on the opposite side). Let's measure and calculate the appropriate resistance we need to apply. 

Across the two hooks, I measure the AC voltage to be 8V (it's AC because it needs to have a frequency to power the loudspeaker). According to the datasheet, the max current allowed is 50 mA, however for safety and best practice we shouldn't go over 30 mA.

Because we're dealing with regular resistance (i.e no components that produce capacitance/inductance), we can calculate as normal for AC. This means the resistance we need in the circuit to be, as calculated simply by Ohm's law: <a href="https://www.codecogs.com/eqnedit.php?latex=\frac{U}{I}=R" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{U}{I}=R" title="\frac{U}{I}=R" /></a> to be <a href="https://www.codecogs.com/eqnedit.php?latex=\frac{8.0&space;V}{0.03A}=267\Omega" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{8.0&space;V}{0.03A}=267\Omega" title="\frac{8.0 V}{0.03A}=267\Omega" /></a>.

Your 220 Ohm resistor will do just fine. Simply connect as such:

![](https://i.imgur.com/Xn4Apaj.png)

It doesn't matter if you put the resistor before or after the optocoupler, as it's the total resistance of the circuit which determines the current.

It's important that the dot on the optocoupler is where the yellow input wire from the smoke detector is; because the dot marks where the + side of the internal lamp is. 

Now please measure the current and see what you get (when you press the test-button on the alarm). I got only 10 mA, which is perfect for me, and probably because of the internal resistance of the optocoupler adding a few ohms as well.

### Piezo and the rest
 Here we got the final diagram. 
![](https://i.imgur.com/PaDcXTE.png)

For the Piezo, we want to connect it to the P21 or P22 as it's the only Digital to Analog outputs, where we can output the frequencies to make the alarm sound we want. Please connect the + side to the P21, and the - side to GND, and insert a 220 Ohm resistor in series for safety measures (as shown in the diagram).

![](https://i.imgur.com/jZEU1pL.jpg)

I then built everything into a box to make it more of a unit. You'll be able to remove the sticker on the back of the breadboard to keep it stuck, and then use two screws with a metal ring to screw your lopy to the cardboard box. 
## Platform

The cloud platform we'll be using is the [free Ubidots STEM platform](https://ubidots.com/stem/). It's a cloud-based, beginner-friendly, easy-to-use platform with good support for Pycom devices.

The main reason why we're going to use it is because it's very easy to create events and get warned. We want to know when our alarm is triggered, and this allows us to do it for free via e-mail.

It's also easy to create a dashboard and present the data and also an app where you can check-in on your alarm and see what's up.

Before proceeding, please sign up [here on Ubidots](https://ubidots.com/stem/) and create your STEM account so you'll get your Ubidots token.

## The code
Here's the full codebase you can download directly if you want: https://github.com/Erikmmkarlsson/Security-System-in-Micropython

I'll assume you've been able to connect with Pymakr to your device. Please reference the [Computer & Hardware Setup](#Computer-amp-Hardware-Setup) for guidance if you've not done it yet.

If you're not copying the codebase, create a new project; create a `lib` folder; a `main.py` and a `boot.py` file.

### The libraries
Please create a file in the lib folder called `keys.py`. In there, copy paste paste this:
```python=
ubidots_token = "insert your ubidots-token"

ssid = "your wi-fi name here"
wpa = "your wi-fi password"
```
[Here's how ](https://help.ubidots.com/en/articles/590078-find-your-token-from-your-ubidots-account)you find your Ubidots token. If you haven't already; [sign up here on Ubidots](https://ubidots.com/stem/) and create your account so you’ll get your Ubidots token. Also insert your wi-fi credentials so it can properly connect to your wi-fi. This file is under the .gitignore so you can safely upload your own fork of this codebase without risking it going public.

Then copy the [urequests.py file](https://github.com/Erikmmkarlsson/Security-System-in-Micropython/blob/master/lib/urequests.py) into your lib folder. After that, copy the [ubi.py file](https://github.com/Erikmmkarlsson/Security-System-in-Micropython/blob/master/lib/ubi.py) as well. 

In the `ubi.py` file you can edit the JSON object you create, to add more variables if you add another sensor for example:

```python=6
# Builds the json to send the request
def build_json(variable1, value1, 
                variable2, value2, 
                variable3, value3):
    try:
        data = {variable1: {"value": value1},
                variable2: {"value": value2},
                variable3: {"value": value3}}
        return data
    except:
        return None
```
And on line 26 in the post_var() function:
```python=26
 # Here you can edit the labels
        data = build_json(
        "Temperature", value1, 
        "Smoke", value2, 
        "Movement", value3
        )
```
You can edit the labels of the variables you send to Ubidots. Please check out [this](https://www.w3schools.com/python/python_json.asp) to learn more about json objects in Python.
### Boot & Main

Now in your boot file, copy-paste this:
```python=
# boot.py -- run on boot-up
from machine import UART
import machine
import keys
from network import WLAN
import os

uart = UART(0, baudrate=115200)
os.dupterm(uart)

machine.main('main.py')

wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
    if net.ssid == keys.ssid:
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, keys.wpa), 
        timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

exec(open("main.py").read()) 
# Just making sure we run main
```

On boot-up our device will try to connect to Wi-fi. It uses the credentials you wrote in the `keys.py` file.

And here's the main:

```python=
import machine
from machine import Pin 
#So we don't need to do machine.Pin everytime 
#we wanna call the Pin constructor
import time
import pycom
import ubi #ubidots

## -- INPUT OBJECTS -- ##
adc = machine.ADC() # ADC object for temp sensor
tempPin = adc.channel(pin='P16') # Read voltage from 
#pin 16. Temperature sensor is here.

# Make 'P19' an input with the pull-down enabled
smokePin = Pin('P9', mode=Pin.IN, pull = Pin.PULL_DOWN)

# Set 'P20' as an input
pirPin = Pin('P20', mode=Pin.IN, pull = Pin.PULL_DOWN)

## -- SOUND -- ##
soundPin =  machine.DAC('P21')  
# Use either P21 or P22. 
# They are the only DAC outputs, which can
# output specific tones for the piezo element.

def soundAlarm():
    soundPin.tone(2000, 2)  
    time.sleep(0.1)         
    soundPin.tone(3000, 1) 
    time.sleep(0.2)
    soundPin.tone(4000, 0)  
    time.sleep(0.3)         

# Here you can play around with different tones, delays, 
# etc. I found this to sound the most like an alarm, 
# but you'll probably find something better :)

# syntax for tone(): 
# tone(frequency, volume lowering)
# (0-3, higher is lower volume)

def quietAlarm():   
    soundPin.write(0)


## -- TIME VARIABLES -- ##
timer = 0       
# Initiatate the timer.

TIMERLAP = 60*10    
# How often to send data to ubidots when it's not red 
# alert. Sending data normally every 10 minutes 
# (60*10 seconds), one because ubidots limiting to 
# 4000 data dots per day on the free plan, or one dot 
# every 22nd second for 24 hours. And the only useful 
# information we're sending is the temperature.       

ALARM_DELAY = 7     
# After the alarm, how long to wait to check and send 
# data again. During this time the alarm sounds.

DETECTION_DELAY = 0.3   
# How short time between each reading of the sensors. 
# I recommend 0.1 (100 ms), but up to 1 second works. 
# Beyond that it's really not worth it, you'll give the 
# intruder enough time to pass by the PIR sensor 
# undetected for example.
# 
# If you connect to battery, 1 second should be plenty 
# to save battery power.

#time.sleep(60)  
# According to the datasheet the PIR sensor gives false 
# readings the first minute, which I've noticed as well.
# 

## -- MAIN -- ##
while True:
    millivolts = tempPin.voltage()      
    # Temperature sensor
    degC = (millivolts - 500.0) / 10.0  
    # Convert voltage to celcius
    movement = pirPin()
    smoke = smokePin()

    if movement or smoke or degC > 40:   
    # If alarm (checks every DETECTION_DELAY second)
        pycom.rgbled(0x7f0000)      
        # Set pycom LED to red
        
        soundAlarm()
        
        ubi.post_var("pycom", degC, smoke, int(movement))    
        # Send sensor data to ubidots
        
        for i in range(ALARM_DELAY*2):
            soundAlarm()

    elif timer > TIMERLAP: 
        ubi.post_var("pycom", degC, smoke, int(movement))   
        # Send regular sensor data to ubidots
        # every TIMERLAP second.
        # For temperature readings over time.
                                                            
        timer = 0 # Restart timer
    else: # It's all green
        pycom.rgbled(0x007f00)      
        quietAlarm()
        timer += DETECTION_DELAY

    time.sleep(DETECTION_DELAY)
```
Then remember to upload the project to your lopy to make sure your `main.py` can communicate with the other files, as it tries to communicate with the files on the board, not the computer. If you've done everything correctly, you should start seeing your data printed in the Pymakr console as JSON objects. Now let's check on Ubidots that our data is being transmitted.

## Transmitting the data / connectivity

We're only using wi-fi, but a good idea might be if you have an open LoRa network to connect to it too for redundancy, if your wi-fi breaks you can still be alarmed.

We use a JSON-object to package our data, this is then sent every 10 minutes (in normal circumstances) with *webhooks* (HTTP pushes) through the wi-fi, over the internet, to the Ubidots API and received in the cloud. If the alarm is triggered, data will be sent every 10 seconds (approximately) as long as the alarm is still triggered.

Because we are connected through the Wi-Fi protocol with unlimited data, the size of the data isn't really a concern. Our security system is in our home, so we aren't really concerned with device range either.

If we had our device on battery, a good idea might be to only send every 30 minutes, since we're only sending temperature as a meaningful data when the alarm isn't triggered. There's no need to know every 10 minutes the temperature since it develops so slowly over time. Every 30 minutes would be more reasonable. 

If we would place our device in a remote location, perhaps to secure a summerhouse without wi-fi connection, only relying on LoRa to send data, then a more wise choice would be to instead use MQTT as *"it is useful for connections with remote locations where a small code footprint is required and/or network bandwidth is at a premium"*(Source: MQTT.org) i.e through the LoRa network as we have a much lower bandwidth.

## Presenting the data

Now go to the devices tab and you should see that your Pycom device showed up.

![](https://i.imgur.com/zD6vQnc.png)

If you go to Data -> Dashboards tab, you'll see something like this:
![](https://i.imgur.com/n3CMf3l.png)

Here you can create your dashboard. Press the + icon and select any widget you want. I recommend the "line chart" for both temperature and the movement/smoke triggers. 

Here's an example of how it could look like:

![](https://i.imgur.com/EGKMH33.png)

Feel free to play around if you find something better.

What's great with Ubidots is that we don't have to think about the database. The data is saved every time we upload, and the data is saved for 30 days on the Ubidots database, and that's really all we need for a home alarm; making it a good choice.

#### Events
If you go to Data -> Events you can create triggers for your events. 100 E-mails per month is included for free in your STEM account, so that's what we'll use to notify you when your alarm goes off.

Simply press + to create a new trigger. I got these triggers, which I recommend:
![](https://i.imgur.com/kqGXHCw.png)
My inactive device trigger for example looks like this:
![](https://i.imgur.com/fmnxPnv.png)
Which will warn me when my Pycom device hasn't sent any data for over 10 minutes, which is good to know.

When you receive an e-mail, save the sender as a favorite, then you can for example in Outlook or Gmail app in the setting in "notifications" change so you only receive notifications from your favorites; and have it look like this:
![](https://i.imgur.com/sHcpCS8.jpg =500x)


## Finalizing the design

![](https://i.imgur.com/aoqmYtZ.jpg)


I built my components into a regular cardboard-box that my router came in. It's able to be put up on the wall or any part of the room, so you can skip using USB and just use a battery if you want to put it up somewhere high or so. Here's it at work when I just enter my apartment:
https://www.youtube.com/embed/naru3gC-lA8
Pretty good! When the alarm went off it also sent a notification to my phone through the e-mail app, so I can know whenever someone moves inside.

Now we got a fully functional smart alarm, with built-in smoke detection and temperature sensors and a good movement detection. What I'd like to add in the future is a camera, so I can take receive pictures of whatever is moving, to really enhance the security aspect; and to verify if it's actually an intruder or burning in my apartment and not a false alarm.





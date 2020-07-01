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
        wlan.connect(net.ssid, auth=(net.sec, keys.wpa), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

exec(open("main.py").read()) # Just making sure we run main
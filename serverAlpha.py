#!/usr/bin/python

from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import bluetooth
from time import sleep

target_name = "My Phone"
target_address = "78:52:1A:4F:4E:6A" 

lcd = Adafruit_CharLCDPlate()
lcd.backlight(lcd.RED)
lcd.message("Jeeps-Berry-Pi\n    Online")
lcd.scrollDisplayRight()
sleep(2)
lcd.clear()
lcd.backlight(lcd.BLUE)
lcd.message(" Searching for\n   passengers")

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
    if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        break

if target_address is not None:
    print "found target bluetooth device with address ", target_address
    lcd.clear()
    lcd.backlight(lcd.GREEN)
    lcd.message("  Found Jaron")
else:
    print "Could not find target bluetooth device nearby"
    lcd.clear()
    lcd.message("Warning:\nPolice Notified")
    lcd.scrollDisplayRight()
    time.sleep(2)
    lcd.clear()
    lcd.message("External GPS tracker\nenabled")

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
port = 2 
server_sock.bind(("",port))
server_sock.listen(1)
print "listening on port %d" % port

uuid = "457807c0-4897-11df-9879-0800200c9a66"
bluetooth.advertise_service( server_sock, "JeepsBerry Service", uuid )

client_sock,address = server_sock.accept()
print "Accepted connection from ",address

while 1:
    data = client_sock.recv(1024)
    print "received [%s]" % data
    print data
    lcd.clear()
#    if data.startswith("    Location:"):
#	print "Scrolling"
#	lcd.message(data)
#	for x in data:
#	    lcd.scrollDisplayLeft()
#	    sleep(.4)
	
 #   else:
    lcd.message(data)

client_sock.close()
server_sock.close()


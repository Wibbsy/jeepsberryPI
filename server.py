#!/usr/bin/python

from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import bluetooth
import os
from time import sleep
import time
import threading
import subprocess
from random import choice
lcd = Adafruit_CharLCDPlate()

'''
target_name = "My Phone"
target_address = "78:52:1A:4F:4E:6A" 

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
'''

class MusicPlayer(threading.Thread):
    #constantly runs in background checks to see if there is a song in the que file
    def __init__(self, lcd):
        super(MusicPlayer, self).__init__()
        self.que_file = "/home/pi/que"
        self.que_swp = "/home/pi/.que.swp"
        self.music_home = "/home/pi/music"
        self.songList = []
	self.currentSong = None
	self.lcd = lcd

    def play(self, song):
        print "starting song"
        print song
        #cmd = "mplayer %s" % (song)
        #os.system(cmd)
        process = []
        process.append(subprocess.Popen(["mplayer", song,]))
        for p in process:
            if p.poll() is None:
                p.wait()

    def getSongList(self):
        for top, dirs, files in os.walk(self.music_home):
            for nm in files:
                song = os.path.join(top, nm)
                #song = "\"%s\"" % (song)
                self.songList.append(song)

    def getCurrentSong(self):
	song = self.currentSong.split("/")[-1]
	song = song.split(".")[0]
	artist = self.currentSong.split("/")[-2]
	songString = "%s\n%s" % (artist,song)
	self.lcd.clear()
	self.lcd.backlight(lcd.TEAL)
	self.lcd.message(songString)

    def run(self):
        self.getSongList()
        while 1:
            self.currentSong = choice(self.songList)
            print "playing %s" % (self.currentSong)
            self.play(self.currentSong)


class Timer(threading.Thread):
    def __init__(self, seconds):
	self.timeExpired = False
    	self.runTime = seconds
    	threading.Thread.__init__(self)

    def run(self):
	while self.runTime > 0:
	    time.sleep(1)
	    self.runTime = self.runTime - 1
	    
	self.timeExpired = True

    def updateTimer(self, newTime):
	self.runTime = newTime

    def expireCheck(self):
	return self.timeExpired

def currentTime(bluetoothClient):
    currentTime = time.strftime("    %H:%M:%S\n   %Y-%m-%d")

    print currentTime

    lcd.clear()
    lcd.backlight(lcd.GREEN)
    lcd.message(currentTime)

def location(bluetoothClient):
    lcd.backlight(lcd.VIOLET)
    lcd.clear()
    lcd.message("Calculating\nLocation...")
    client_sock.send("location")
    locationString = client_sock.recv(1024)
    lcd.clear()
    lcd.message(locationString)

player = MusicPlayer(lcd)

btn = ((lcd.SELECT, 'Select', lcd.ON),
       (lcd.LEFT  , 'Left'  , currentTime),
       (lcd.UP    , 'Up'    , location),
       (lcd.DOWN  , 'Down'  , player.getCurrentSong),
       (lcd.RIGHT , 'Right' , lcd.VIOLET))

lcd.backlight(lcd.RED)
lcd.message("Jeeps-Berry-Pi\n    Online")
lcd.scrollDisplayRight()
sleep(4)
lcd.clear()
lcd.backlight(lcd.BLUE)
lcd.message("  Waiting for\n   connection")

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
port = 2 
server_sock.bind(("",port))
server_sock.listen(1)
print "listening on port %d" % port

uuid = "457807c0-4897-11df-9879-0800200c9a66"
bluetooth.advertise_service( server_sock, "JeepsBerry Service", uuid )

client_sock,address = server_sock.accept()
print "Accepted connection from ",address
sysTime=client_sock.recv(1024)
print sysTime
cmd = "date -s \"%s\"" % (sysTime)
os.system(cmd)

player.start()
lastKnownFunction = currentTime
prev = -1
t = Timer(2)
t.start()
while True:
    for b in btn:
        if lcd.buttonPressed(b[0]):
	    t.updateTimer(1)
            if b is not prev:
                print b[1]
                lcd.clear()
		print b[2]
		try:
                   b[2](client_sock)
		except:
		   b[2]()
		lastKnownFunction = b[2]
                #lcd.backlight(b[2])
                prev = b
            break
    if t.expireCheck():
	try:
    	    lastKnownFunction(client_sock)
	except:
	    lastKnownFunction()
	if lastKnownFunction.__name__ is "currentTime":
	    t = Timer(1)
	    t.start()
	elif lastKnownFunction.__name__ is "getCurrentSong":
	    t = Timer(1)
	    t.start()
	else:
	    t = Timer(60)
	    t.start()


'''
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
'''

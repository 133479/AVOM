# Imports
from flask import Flask, render_template

from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
from time import sleep
from mfrc522 import SimpleMFRC522
import socket

GPIO.setmode(GPIO.BCM)

# Init servo
servoPIN = 17

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(servoPIN, GPIO.OUT)
#p = GPIO.PWM(servoPIN, 50)
#p.start(0)
#GPIO.cleanup()

# Init RFID
reader = SimpleMFRC522()


# Resolve hostname
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
hn = (s.getsockname()[0])
h = (hn + ":5000")
print("\n")
print('\033[1m' + ("#####") + ' \033[0m')
print('\033[92m' + '\033[1m' + ("BEGIN OF MESSAGE") + ' \033[0m')
print("\n")
print('\033[93m' + '\033[1m' + ("MAIN HOST") + ' \033[0m')
print('\033[96m' + '\033[1m' + ("Make sure it says 'running on http://(ip after main host, 1 line below)' below. If it doesn't, use the command in cmd.txt.") + ' \033[0m')
print('\033[94m' + '\033[1m' + (">>> main host: " + h + " <<<") + ' \033[0m')
print("\n")
print('\033[93m' + '\033[1m' + ("LOCAL HOST") + ' \033[0m')
print('\033[94m' + '\033[1m' + (">>> local host: " + "127.0.0.1:5000" + " <<<") + ' \033[0m')
print("\n")
print('\033[92m' + '\033[1m' + ("END OF MESSAGE") + ' \033[0m')
print('\033[1m' + ("#####") + ' \033[0m')
print("\n")
s.close()

# Init RGB LED
LED_R_PIN = 13
LED_G_PIN = 12
LED_B_PIN = 18

GPIO.setup(servoPIN, GPIO.OUT)
GPIO.setup([LED_R_PIN, LED_G_PIN, LED_B_PIN],GPIO.OUT)


RED = GPIO.PWM(LED_R_PIN, 1000)
GREEN = GPIO.PWM(LED_G_PIN, 1000)
BLUE = GPIO.PWM(LED_B_PIN, 1000)
SERVO = GPIO.PWM(servoPIN, 50)
RED.start(0)
GREEN.start(0)
BLUE.start(0)
SERVO.start(0)


# Init RGB mapping
def _map(x, in_min, in_max, out_min, out_max):
	return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Function for GPIO/RGB LED init (MUST BE CALLED AS 'R, G, B, GPIO = init()' BEFORE USAGE)
"""
def init():
	#GPIO.cleanup()
	#GPIO.setmode(GPIO.BCM)
	#GPIO.setup([LED_R_PIN, LED_G_PIN, LED_B_PIN],GPIO.OUT)
	#RED = GPIO.PWM(LED_R_PIN, 1000)
	#GREEN = GPIO.PWM(LED_G_PIN, 1000)
	#BLUE = GPIO.PWM(LED_B_PIN, 1000)
	RED.start(0)
	GREEN.start(0)
	BLUE.start(0)
	return(RED, GREEN, BLUE, GPIO)
"""

def setAngle(a, p):
	dc = 2 + (a/18)
	p.ChangeDutyCycle(dc)
	sleep(0.5)
	p.ChangeDutyCycle(0)


def open(mod):
	if mod == "Kopen":
		RED.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
		GREEN.ChangeDutyCycle(_map(10, 0, 255, 0, 100))
		BLUE.ChangeDutyCycle(_map(20, 0, 255, 0, 100))	
	elif mod == "Openen":
		RED.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
		GREEN.ChangeDutyCycle(_map(20, 0, 255, 0, 100))
		BLUE.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
	setAngle(90, SERVO)
	#R, G, B, gp = init()

	clln(0)
	clln(1)
	w(("> MODUS: " + mod), 0, 0)
	if mod == "Kopen":
		w("Eten uithalen...", 1, 0)
	elif mod == "Openen":
		w("Eten invoeren...", 1, 0)


	sleep(5)
	clln(0)
	w("Deur sluiten...  ", 0, 0)
	clln(1)
	RED.ChangeDutyCycle(_map(255, 0, 255, 0, 100))
	GREEN.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
	BLUE.ChangeDutyCycle(_map(0, 0, 255, 0, 100))	
	sleep(0.7)
	RED.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
	GREEN.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
	BLUE.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
	sleep(0.3)
	RED.ChangeDutyCycle(_map(255, 0, 255, 0, 100))
	GREEN.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
	BLUE.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
	sleep(0.4)
	RED.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
	GREEN.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
	BLUE.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
	sleep(0.4)
	RED.ChangeDutyCycle(_map(255, 0, 255, 0, 100))
	GREEN.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
	BLUE.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
	sleep(0.4)
	RED.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
	GREEN.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
	BLUE.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
	
	
	sleep(0.1)
	setAngle(0, SERVO)
	#clean(R, G, B, gp)
	
	return ""

# Function to do cleanup for GPIO and RGB LED (MUST BE CALLED AFTER LED HAS BEEN USED AS 'clean(R, G, B, GPIO)')
def clean(R, G, B, GPIO):
	R.stop()
	G.stop()
	B.stop()
	GPIO.cleanup()
	return ""
	

# Init LCD
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
lcd.clear()
	

# Function to write to LCD
# Format: 'w({text: str}, {line 0-1: int}, {col 0-15: int})'
def w(txt, ln, col):
	try:
		lcd.cursor_pos = (int(ln), int(col))
		lcd.write_string(str(txt))
	except Exception as e:
		print("W format: w({text: str}, {line 0-1: int}, {col 0-15: int})")
		print(e)
		

# Function to display hostname 
def dhn():
	w("http://" + h, 0, 0)


# Function to clear line ln (LCD)
def clln(ln):
	w("                ", ln, 0)


# Write homepagina ip on LCD
dhn()

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

#background process happening without any refreshing
@app.route('/button_buy')
def background_process_buy():


	clln(0)
	clln(1)
	w("> MODUS: Kopen", 0, 0)
	w("Kaart tonen...  ", 1, 0)
	
	try:
		id, text = reader.read()
		print(id)
		print(text)
		w("Gebruiker gevon-", 0, 0)
		w("den! Wacht even.", 1, 0)
		sleep(1)
	finally:
		w("Deur openen...  ", 0, 0)
		clln(1)
		sleep(0.5)

		open("Kopen")
		
		
		#R, G, B, GPIO = init()
		#R.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
		#G.ChangeDutyCycle(_map(10, 0, 255, 0, 100))
		#B.ChangeDutyCycle(_map(20, 0, 255, 0, 100))			
		#sleep(3)
		sleep(0.5)
		clln(0)
		clln(1)
		w("> MODUS: Kopen", 0, 0)
		w("BERICHT: Klaar!", 1, 0)
		sleep(1)
		clln(0)
		clln(1)
		#clean(R, G, B, GPIO)
		dhn()
		return("nothing")



#background process happening without any refreshing
@app.route('/button_open')
def background_process_open():


	clln(0)
	clln(1)
	w("> MODUS: Openen", 0, 0)
	w("Kaart tonen...  ", 1, 0)
	
	try:
		id, text = reader.read()
		print(id)
		print(text)
		w("Gebruiker gevon-", 0, 0)
		w("den! Wacht even.", 1, 0)
		sleep(1)
	finally:
		w("Deur openen...  ", 0, 0)
		clln(1)
		sleep(0.5)

		open("Openen")
		
		
		#R, G, B, GPIO = init()
		#R.ChangeDutyCycle(_map(0, 0, 255, 0, 100))
		#G.ChangeDutyCycle(_map(10, 0, 255, 0, 100))
		#B.ChangeDutyCycle(_map(20, 0, 255, 0, 100))			
		#sleep(3)
		sleep(0.5)
		clln(0)
		clln(1)
		w("> MODUS: Openen", 0, 0)
		w("BERICHT: Klaar!", 1, 0)
		sleep(1)
		clln(0)
		clln(1)
		#clean(R, G, B, GPIO)
		dhn()
		return("nothing")

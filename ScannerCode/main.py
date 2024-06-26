import PySimpleGUI as sg
import requests
import json
import RPi.GPIO as GPIO
import signal
import time
import sys
import keyboard
import serial

layout = [[sg.Text(text='Inventory Scanner',
		font=('Arial Bold', 20),
		size=20,
		expand_x=True,
		justification='center')],
]

BUTTON_GPIO = 16
USERLOGGED = 'Ethan'
BARCODESCANNED = ''
HIDDENKEY = '1234'
BASEURL = "http://192.168.1.86:8000"

def setup():
	GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, callback=button_pressed_callback, bouncetime=1000)

def signal_handler(sig,frame):
	GPIO.cleanup()
	sys.exit(0)
	
def button_pressed_callback(channel):
	time.sleep(2)
	keyboard.press_and_release('enter')

def startUp():
    global USERLOGGED
    USERLOGGED = ""
    while True:
        try:
            contents = requests.get(BASEURL, timeout=5)
            if contents.status_code == 200:
                break
        except:
            sg.popup("Can't Connect To Server", no_titlebar=True, auto_close=True, auto_close_duration=2)
            continue
    return
        
def waitForUser():
    print("Please scan your Employee Code:")
    while True:
        sg.popup("Please scan your Employee Code:", no_titlebar=True, auto_close=True, auto_close_duration=2)
        code = readCodeInput()
        mesCode = loginUser(code) 
        if  mesCode == -1:
             continue
        else:
            break

def readCodeInput():
    output = " "
    ser = serial.Serial('/dev/ttyACM0', 4800, 8, 'N', 1, timeout=1)
    while True:
        while output != "":
            output = ser.readline()
            print (output)
        return output

def waitForTool():
    print("You are signed in as " + USERLOGGED +". Please scan a barcode:")
    code = sg.popup_get_text("You are signed in as " + USERLOGGED +". Please scan a barcode:", no_titlebar=True, font=('Arial Bold', 10))
    codeType = requests.get(BASEURL + "/codes/findtype/" + code + "/")
    if codeType.text == "tool":
        result = checkTool(code)
        if result[0]["fields"]["isCheckedOut"]:
             sg.popup("Successfully checked out " + result[0]["fields"]["name"], no_titlebar=True, auto_close=True, auto_close_duration=2)
        else:
             sg.popup("Successfully checked in " + result[0]["fields"]["name"], no_titlebar=True, auto_close=True, auto_close_duration=2)

    elif codeType.text == "supply":
        result = replenishSupply(code)
        sg.popup("Successfully replenished " + result[0]["fields"]["name"], no_titlebar=True, auto_close=True, auto_close_duration=2)
    
    elif codeType.text == "job":
        result = scanJob(code)
        sg.popup("Successfully Scanned " + result[0]["fields"]["name"], no_titlebar=True, auto_close=True, auto_close_duration=2)

    elif codeType.text == "user":
        logoutUser(code)
    else:
        sg.popup("Code Not Recongized", no_titlebar=True, auto_close=True, auto_close_duration=1)


def loginUser(user):
    global USERLOGGED
    url = BASEURL + "/users/get/" + user + "/"
    while True:
        try:
            contents = requests.get(url)
            contents.status_code
            break
        except:
            sg.popup("Employee not in system, please try again", no_titlebar=True, auto_close=True, auto_close_duration=1)
            return -1
    obj = json.loads(contents.text)
    USERLOGGED = obj[0]["fields"]["name"]
    return obj

def logoutUser(user):
    global USERLOGGED
    url = BASEURL + "/users/get/" + user + "/"
    contents = requests.get(url)
    obj = json.loads(contents.text)
    if obj[0]["fields"]["name"] == USERLOGGED:
        USERLOGGED = ""
    else:
        sg.popup("Please sign out of current user before signing in again, Current user is " + USERLOGGED, no_titlebar=True, auto_close=True, auto_close_duration=1)
    return obj

def checkTool(tool):
    url = 'http://192.168.1.86:8000/tools/edit/' + tool + "/check/" + HIDDENKEY + "/" + USERLOGGED
    try:
        contents = requests.get(url)
        contents.raise_for_status()
    except:
        sg.popup("Can't Connect To Server", no_titlebar=True, auto_close=True, auto_close_duration=1)
    obj = json.loads(contents.text)
    return obj
    
def scanJob(tool):
    url = 'http://192.168.1.86:8000/jobs/edit/' + tool + "/scan/" + HIDDENKEY + "/" + USERLOGGED
    try:
        contents = requests.get(url)
        contents.raise_for_status()
    except:
        sg.popup("Can't Connect To Server", no_titlebar=True, auto_close=True, auto_close_duration=1)
    obj = json.loads(contents.text)
    return obj

def replenishSupply(supply):
    url = 'http://192.168.1.86:8000/supply/edit/' + supply + "/replen/" + HIDDENKEY + "/" + USERLOGGED
    try:
        contents = requests.get(url)
        contents.raise_for_status()
    except:
        sg.popup("Can't Connect To Server", no_titlebar=True, auto_close=True, auto_close_duration=1)
    obj = json.loads(contents.text)
    return obj

window = sg.Window("Inventory Sysetm", layout, no_titlebar=False, location=(0,0), size=(480,360), keep_on_top=True).finalize()
window.bind("<Escape>", "-ESCAPE-")
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
signal.signal(signal.SIGINT, signal_handler)
setup()
startUp()
while True:
	waitForUser()
	while True:
			waitForTool()
			if USERLOGGED == "":
				break
	event, values = window.read(timeout=10)
	print(event, values)
	if event in (None, "Exit"):
		break
	if event in (sg.WINDOW_CLOSED, "-ESCAPE-"):
		break
	
	
window.close()

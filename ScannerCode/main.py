import requests
import json
import RPi.GPIO as GPIO
import signal
import time
import sys
import keyboard



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
            print("Cannot Connect to Inventory Server")
            continue
    return
        
def waitForUser():
    print("Please scan your Employee Code:")
    code = input()
    loginUser(code)    

def waitForTool():
    print("You are signed in as " + USERLOGGED +". Please scan a barcode:")
    code = input()
    codeType = requests.get(BASEURL + "/codes/findtype/" + code + "/")
    if codeType.text == "tool":
        result = checkTool(code)
    elif codeType.text == "supply":
        pass
    elif codeType.text == "user":
        logoutUser(code)
    else:
        print("Code Not Recongized")


def loginUser(user):
    global USERLOGGED
    url = BASEURL + "/users/get/" + user + "/"
    while True:
        try:
            contents = requests.get(url)
            contents.status_code
            break
        except:
            print("Employee Code not in system, please try again")
            continue
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
        print("Please sign out current user before signing in. Current User is: " + USERLOGGED)
    return obj

def checkTool(tool):
    url = 'http://192.168.1.86:8000/tools/edit/' + tool + "/check/" + HIDDENKEY + "/" + USERLOGGED
    try:
        contents = requests.get(url)
        contents.raise_for_status()
    except:
        return logoutUser(tool)
    obj = json.loads(contents.text)
    return obj


if __name__ == '__main__':
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

import PySimpleGUI as sg
import requests
import json
import signal
import time
import sys
import serial

layout = [[sg.Text(text='Inventory Scanner',
		font=('Arial Bold', 20),
		size=20,
		expand_x=True,
		justification='center')],
]

USERLOGGED = 'Ethan'
BARCODESCANNED = ''
HIDDENKEY = '1234'
BASEURL = "http://192.168.1.86:8000"

def signal_handler(sig,frame):
	sys.exit(0)

def startUp():
    global USERLOGGED
    USERLOGGED = ""
    while True:
        try:
            contents = requests.get(BASEURL, timeout=5)
            if contents.status_code == 200:
                break
        except:
            sg.popup("Can't Connect To Server", no_titlebar=True, auto_close=True,  auto_close_duration=2)
            continue
    return

def waitForUser():
    print("Please scan your Employee Code:")
    while True:
        sg.popup("Please scan your Employee Code:", no_titlebar=True, auto_close=True, non_blocking=True, auto_close_duration=5)
        code = readCodeInput()
        mesCode = loginUser(code) 
        print(mesCode)
        if  mesCode == -1:
             continue
        else:
            break

def waitForTool():
    print("You are signed in as " + USERLOGGED +". Please scan a barcode:")
    sg.popup("You are signed in as " + USERLOGGED +". Please scan a barcode:", no_titlebar=True, auto_close=True, non_blocking=True, auto_close_duration=5)
    code = readCodeInput()
    if code == "":
         return 0
    codeType = requests.get(BASEURL + "/codes/findtype/" + code + "/")
    try:
         codeType.raise_for_status()
    except:
         return -1
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
            contents.raise_for_status()
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

def readCodeInput():
    output = ""
    ser = serial.Serial('/dev/ttyACM0', 4800, 8, 'N', 1, timeout=1)
    for x in range(10):
        output = ser.readline().rstrip()
        output = output.decode("ascii")
        print (output)
        if output == "":
             continue
        else:
             return output
    return ""
            

window = sg.Window("Inventory Sysetm", layout, no_titlebar=False, location=(0,0), size=(480,360), keep_on_top=True).finalize()
window.bind("<Escape>", "-ESCAPE-")
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
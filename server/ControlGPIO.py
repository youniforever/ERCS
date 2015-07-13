import os
import re
import RPi.GPIO as GPIO

def pinHigh(pinId):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(int(pinId), GPIO.OUT)
    GPIO.output(int(pinId), 1)
    return {"result": 200, "err": ""}

def pinLow(pinId):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(int(pinId), GPIO.OUT)
    GPIO.output(int(pinId), 0)
    return {"result": 200, "err": ""}

def pinStatus(uId, pinId):
    pinPath = '/sys/devices/virtual/gpio/gpio' + GPIO._GPIO_PINS[pinId] + '/value'

    if ( os.path.isfile(pinPath) ):
        f = open(pinPath)
        strPinStatus = f.read()
        f.close()

        pinStatus = re.sub(r'[^\d]', r'', strPinStatus)
        
        resp = {"result": 200, "data": {"uId": str(uId), "pinStatus": int(pinStatus)}, "error": ""}
    else:
        resp = {"result": 200, "data": {"uId": str(uId), "pinStatus": 0}, "error": ""}

    return resp

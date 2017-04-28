#!/usr/bin/env python

import subprocess
import time
from lib import Adafruit_CharLCDPlate


class SpeedTestCheck(object):

    def __init__(self):
        self.current = {}

    def setLCD(self, color):
        self.lcd.clear()
        self.lcd.backlight(self.lcd.%s % color)

    def setup(self):
        self.lcd = Adafruit_CharLCDPlate()
        self.setLCD(BLUE)

    def checkspeed(self):
        self.setLCD(VIOLET)
        self.lcd.message("Checking speed....")
        cmd = "speedtest-cli --simple --secure"
        raw = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, errors = raw.communicate()
        cleaned = filter(None, output.split('\n'))
        self.current = dict(map(str, x.split(':')) for x in cleaned)
        print self.current

    def printspeed(self):
        if self.current['Download'].split('.')[0] > 35:
            self.setLCD(GREEN)
        elif self.current['Download'].split('.')[0] < 35:
            self.setLCD(RED)
        msg1 = "Down" + self.current['Download'].split('.')[0] + '\n' + "Up" + self.current['Upload'].split('.')[0]
        self.lcd.message(msg1)

    def main(self):
        self.setup()
        while True:
            try:
                self.checkspeed()
            except Exception as e:
                print "could not check speed: %s" %(e)
            try:
                self.printspeed()
            except Exception as e:
                print "could not display speed: %s" %(e)
            time.sleep(3600)



if __name__ == '__main__':
    stc = SpeedTestCheck()
    stc.main()

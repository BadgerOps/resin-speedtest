#!/usr/bin/env python

import threading
import time
import os
try:
    import Adafruit_CharLCD as LCD
except ImportError:
    print "Please install the Adafruit_CharLCD package"
    exit(1)

class LcdPlate(threading.Thread):

    def __init__(self, SpeedTestCheck):
        self.sc = SpeedTestCheck
        threading.Thread.__init__(self)
        self.lcd_buttons = None
        self.setup()
        self.primary_ip = self.getprimaryip()
        self.buttons = [ LCD.SELECT, LCD.LEFT, LCD.UP, LCD.DOWN, LCD.RIGHT ]

    def setup(self):
        """
        Set up initial requirements, create self.lcd by instantiating the CharLCDPlate
        set default color of plate
        :return:
        """
        print "running plate setup"
        #pass
        self.lcd = LCD.Adafruit_CharLCDPlate()
        self.lcd.clear()
        self.lcd.message("Setting up...")
        self.lcd.set_color(1.0, 0.0, 1.0)

    def button_matrix(self, button, messages):
        buttons = ((LCD.SELECT, self.sc.printspeed(), (1, 1, 1)),
               (LCD.LEFT, self.print_screen('{0}'.format(messages['prev'])), (1, 0, 0)),
               (LCD.UP, self.print_screen('primary IP is: \n {0}'.format(self.primary_ip)), (0, 0, 1)),
               (LCD.DOWN, self.print_screen('{0}'.format(messages['server'])), (0, 1, 0)),
               (LCD.RIGHT, self.print_screen('{0}'.format(messages['curr'])), (1, 0, 1)))
        return buttons

    def print_screen(self, content):
        """
        Print a message to the screen based on the content given
        :param content:  
        """
        self.lcd.clear()
        self.lcd.message(content)

    def getprimaryip(self):
        """
        We can't know for sure that /etc/hosts is set up properly, so socket.gethostbyname() isn't guaranteed.
        This is an adaptation of a Salt grain I wrote to do the same thing.
        :return str: 
        """
        with os.popen("ip route | grep default | grep -Eo 'dev\s+\w+' | awk '{print $2}'") as defroute_device_pipe:
            def_route = defroute_device_pipe.read().strip()
        with os.popen("ip a s {0} | grep -E 'inet\s' | cut -d'/' -f1 | awk '{{print $2}}'".format(def_route)) as devip_pipe:
            devip = devip_pipe.read().strip()
        return devip

    def run(self):
        """
        Threaded run process
        Run a while loop and check button state.
        """
        while True:

            try:
                if self.sc.running == False:
                    print "waiting for main loop to get set up \n"
                    time.sleep(5)
                    pass
                else:
                    time.sleep(0.1) # dont run away...
                    #self.lcd_buttons = self.buttons(self.sc.messages)  # refresh buttons
                    for b in self.buttons:
                        if self.lcd.is_pressed(b):
                            button = self.button_matrix(b, self.sc.messages)
                            self.lcd.clear()
                            self.lcd.set_color(button[2][0], button[2][1], button[2][2])
                            self.buttons(button[1])

            except Exception as e:
                print 'Exception in LCD Loop: {0}'.format(e, exc_info=1)
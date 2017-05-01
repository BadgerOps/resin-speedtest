#!/usr/bin/env python


import speedtest
import schedule
import time
import Adafruit_CharLCD as LCD

class SpeedTestCheck(object):

    def __init__(self):
        self.previous = {'up': 1, 'down': 1, 'ping': 1, 'server': None}
        self.current = {'up': 1, 'down': 1, 'ping': 1, 'server': None}
        self.lcd_buttons = None
        self.messages = {}

    def setup(self):
        """
        Set up initial requirements, create self.lcd by instantiating the CharLCDPlate
        set default color of plate
        :return:
        """
        print "running setup"
        #pass
        self.lcd = LCD.Adafruit_CharLCDPlate()
        self.lcd.clear()
        self.lcd.message("Setting up...")
        self.lcd.set_color(1.0, 0.0, 1.0)
        self.generate_messages()
        self.lcd_buttons = self.buttons(self.messages)

        print "setup complete"

    def schedule_jobs(self):
        """
        Schedule jobs to run. For now its just 'checkspeed()'
        :return:
        """
        schedule.every(60).minutes.do(self.checkspeed)

    def conversion(self, bytes):
        """
        Convert Bytes to Mb for human readable output
        TODO: support larger than MB conversion? GB internet is out there...
        :return: Int
        """
        return int(bytes / 1000 / 1000)

    def checkspeed(self):
        """
        Using the https://github.com/sivel/speedtest-cli/wiki API we run a
        speedtest against a local speedtest.net server
        """
        print "running speedtest"
        self.lcd.clear()
        self.lcd.message("Checking Speed")
        self.previous = self.current # keep 1 previous speedtest attempt
        print self.previous
        servers = []
        s = speedtest.Speedtest()
        s.get_servers(servers)
        s.get_best_server()
        s.download()
        s.upload()

        self.set_current(s.results.dict())
        self.printspeed()

    def printspeed(self):
        if self.current['down'] > 35:
            self.lcd.clear()
            self.lcd.set_color(0.0, 1.0, 0.0)
        elif self.current['down'] < 35:
            self.lcd.clear()
            self.lcd.set_color(1.0, 0.0, 0.0)
        msg1 = "Down: {0} Mb/s".format(self.current['down']) + '\n' + "Up: {0} Mb/s".format(
            self.current['up'])
        self.lcd.message(msg1)

    def set_current(self, results):
        print 'updating current speed values'
        self.current = {
            'up': self.conversion(results['upload']),
            'down': self.conversion(results['download']),
            'ping': int(results['ping']),
            'server': results['server']['id'],
            'timestamp': results['timestamp']
        }

    def buttons(self, messages):
        buttons = ((LCD.SELECT, 'run speedtest', (1, 1, 1)),
               (LCD.LEFT, '{}'.format(messages['prev']), (1, 0, 0)),
               (LCD.UP, 'not used yet', (0, 0, 1)),
               (LCD.DOWN, '{}'.format(messages['server']), (0, 1, 0)),
               (LCD.RIGHT, '{}'.format(messages['curr']), (1, 0, 1)))
        return buttons

    def generate_messages(self):
        self.messages = {
            'prev': "Previous Speed: \n Down: {} Up: {}".format(self.previous['down'], self.previous['up']),
            'curr': "Current Speed: \n Down: {} Up: {}".format(self.current['down'], self.current['up']),
            'server': "Server: {}".format(self.current['server']),
        }

    def main(self):
        """
        Run the thing!
        :return:
        """
        self.setup()
        self.schedule_jobs()
        print "entering main loop"
        self.lcd.clear()
        self.lcd.message("main loop")
        self.checkspeed()
        while True:
            schedule.run_pending()
            self.generate_messages()
            time.sleep(1)
            for button in self.lcd_buttons:
                if self.lcd.is_pressed(button[0]):
                    self.lcd.clear()
                    if button[1] == 'run speedtest':
                        self.checkspeed()
                        self.printspeed()
                        return
                    self.lcd.message(button[1])
                    self.lcd.set_color(button[2][0], button[2][1], button[2][2])



if __name__ == '__main__':
    sf = SpeedTestCheck()
    sf.main()

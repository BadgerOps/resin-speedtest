#!/usr/bin/env python


import speedtest
import schedule
import time
import libs
import logging

class SpeedTestCheck(object):

    def __init__(self):
        self.netspeed = {'up': 20, 'down': 40 }
        self.previous = {'up': 1, 'down': 1, 'ping': 1, 'server': None}
        self.current = {'up': 1, 'down': 1, 'ping': 1, 'server': None}
        self.messages = {}
        self.running = False

    def setup_logging(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='(%(threadName)-10s) %(message)s',
                            )
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
        self.plate.lcd.clear()
        self.plate.lcd.message("Checking Speed")
        self.previous = self.current # keep 1 previous speedtest attempt
        print self.previous
        servers = []
        s = speedtest.Speedtest()
        s.get_servers(servers)
        s.get_best_server()
        s.download()
        s.upload()

        self.set_current(s.results.dict())
        self.generate_messages()
        self.printspeed()

    def printspeed(self):
        if self.current['down'] > self.netspeed['down']:
            self.plate.lcd.clear()
            self.plate.lcd.set_color(0.0, 1.0, 0.0)
        elif self.current['down'] < self.netspeed['down']:
            self.plate.lcd.clear()
            self.plate.lcd.set_color(1.0, 0.0, 0.0)
        msg1 = "Down: {0} Mb/s".format(self.current['down']) + '\n' + "Up: {0} Mb/s".format(
            self.current['up'])
        self.plate.lcd.message(msg1)

    def set_current(self, results):
        print 'updating current speed values'
        self.current = {
            'up': self.conversion(results['upload']),
            'down': self.conversion(results['download']),
            'ping': int(results['ping']),
            'server': results['server']['id'],
            'timestamp': results['timestamp']

        }

    def generate_messages(self):
        self.messages = {
            'prev': "Previous Speed: \n Down: {0} Up: {1}".format(self.previous['down'], self.previous['up']),
            'curr': "Current Speed: \n Down: {0} Up: {1}".format(self.current['down'], self.current['up']),
            'server': "Server: {0}".format(self.current['server']),
            'ip_addr': "IP Address is: \n {0}".format(self.plate.getprimaryip())
        }

    def start_plate(self):
        """
        Start the LCD plate up
        :return:
        """
        self.plate = libs.LcdPlate(self)
        self.plate.setDaemon(True)
        self.plate.start()

    def main(self):
        """
        Run the thing!
        :return:
        """
        #self.setup_logging()
        self.start_plate()
        self.schedule_jobs()
        print "entering main loop"
        self.plate.lcd.clear()
        self.plate.lcd.message("main loop")
        self.checkspeed()
        self.generate_messages()
        self.running = True
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    sf = SpeedTestCheck()
    sf.main()

# Python Speedtest app for Raspberry Pi

This is a simple app I wrote to run a speedtest and display it using this [very nice](https://learn.adafruit.com/adafruit-16x2-character-lcd-plus-keypad-for-raspberry-pi) display.

I [wrote a blog post](https://blog.badgerops.net/2017/05/16/creating-a-raspberry-pi-based-resin-io-powered-speed-test-app/) about this app, explaining the code and how to use it.

## Parts

I'm using a Raspberry Pi v3, and the aforementioned [Adafruit RGB LCD+Keypad kit](https://www.adafruit.com/product/1109)

### Resin.io Setup & Deployment

1. If you haven't got a resin.io account, visit [resin.io](http://resin.io) and sign up.
2. start a new applicaton on resin.io, name it what you want, download the .zip file and extract it to your SD card.
3. Insert the SD card into the Raspberry pi, connect the ethernet cable and power it up.
4. After about 10 -15 minutes your device should show up on the resin.io applications dashboard.

Once your resin.io account is set up, you should be able to:

`$ git clone https://github.com/Badger32d/resin-speedtest.git`

then add the resin remote: (replacing <myUserName> and <myApplicationName> with yours from the resin.io dashboard)

`$ git remote add resin git@git.staging.resin.io:<myUserName>/<myApplicationName>.git`

and finally push the code to your Raspberry Pi:

`$ git push resin master`

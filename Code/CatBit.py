#

# Pin0=X
# Pin1=Y
# Pin3=Laser

from microbit import *
import utime

class Servo:
    """
    https://github.com/microbit-playground/microbit-servo-class
    For simplicity etc I just copy the class here rather than adding to IDE
    """

    def __init__(self, pin, freq=50, min_us=600, max_us=2400, angle=180):
        self.min_us = min_us
        self.max_us = max_us
        self.us = 0
        self.freq = freq
        self.angle = angle
        self.analog_period = 20
        self.pin = pin
        analog_period = round((1/self.freq) * 1000)  # hertz to miliseconds
        self.pin.set_analog_period(analog_period)

    def write_us(self, us):
        us = min(self.max_us, max(self.min_us, us))
        duty = round(us * 1024 * self.freq // 1000000)
        self.pin.write_analog(duty)

    def write_angle(self, degrees=None):
        degrees = degrees % 360
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self.angle
        self.write_us(us)

    def disable(self):
        self.pin.write_analog(0)  # pwm duty cycle to zero
        self.pin.write_digital(0)  # turn the pin off

class Laser:
    """
    Set laser power via a exponential
    """

    def __init__(self, pin, max_pwm=1023, max_level=100):
        self.pin = pin
        self.max_pwm = max_pwm
        self.max_level = max_level

    def set_level(self, level=0):
        # limit to range
        if level > self.max_level:
            level = self.max_level
        if level < 0:
            level = 0
        pwm = pow(self.max_pwm + 1, level / self.max_level) - 1
        self.pin.write_analog(pwm)

    def off(self):
        self.pin.write_analog(0)

# Initialise pins etc
# Values here are good for AliExpress G90 servos @5V
svX = Servo(pin0, freq=50, min_us=700, max_us=2500, angle=180)
svY = Servo(pin1, freq=50, min_us=700, max_us=2500, angle=180)
led = Laser(pin2)

# Limits
min_x = 0
max_x = 180
min_y = 0
max_y = 125
center_x = min_x + (max_x - min_x)/2
center_y = min_y + (max_y - min_y)/2

# Status
centered = False

# Functions
def laserflash(speed=1):  # Silly demo function
    for x in range(-100, 200, 3):
        led.set_level(x)
        sleep(speed)
    for x in range(200, -100, -2):
        led.set_level(x)
        sleep(speed)

while True:
    if button_a.was_pressed():
        centered = False
        display.show("+")
        svX.write_angle(min_x)
        svY.write_angle(min_y)
        led.off()
        sleep(1000)
        for x in range(min_x, max_x, 1):
            svX.write_angle(x)
            svY.write_angle(x/1.4)
            led.set_level(100*(x-min_x)/(max_x-min_x))
            sleep(30)
        sleep(1000)
        svX.write_angle(max_x)
        svY.write_angle(min_y)
        led.off()
        for x in range(min_x, max_x, 1):
            svX.write_angle(max_x-x)
            svY.write_angle(x/1.4)
            led.set_level(100*(x-min_x)/(max_x-min_x))
            sleep(30)
        sleep(1000)
    if button_b.was_pressed():
        centered = False
        display.show("O")
        svX.write_angle(max_x)
        svY.write_angle(max_y)
        sleep(500)
        led.set_level(100)
        sleep(1000)
        svX.write_angle(max_x)
        svY.write_angle(min_y)
        sleep(1000)
        svX.write_angle(min_x)
        svY.write_angle(min_y)
        sleep(1000)
        svX.write_angle(min_x)
        svY.write_angle(max_y)
        sleep(1000)
        svX.write_angle(max_x)
        svY.write_angle(max_y)
        sleep(1000)
        led.off()
    else:
        display.show("-")
        # Turn off and center when no buttons pressed
        if not centered:
            led.off()
            svX.write_angle(center_x)
            svY.write_angle(center_y)
            centered = True
            sleep(500)
            svX.disable()
            svY.disable()
            sleep(500) # Need time for pwm to settle once turned off
        laserflash()
#fin
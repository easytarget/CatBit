# Cat EnterTainer for BBC Micro:Bit

# Hardware
# Pin0=X
# Pin1=Y
# Pin3=Laser

from microbit import *
import utime
import random


class Servo:
    """
    Original from https://github.com/microbit-playground/microbit-servo-class
    Adapted, bugfixed and improved by Owen
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
        # Dont turn off mid-pulse (avoids spurious movement)
        start = utime.ticks_ms()   # short blocking loop
        while utime.ticks_diff(utime.ticks_ms(), start) < 250:
            if not self.pin.read_digital():  # if pin is off
                break                        # break out immediately
        self.pin.write_digital(0)  # turn the pin off


class LinearLed:
    """
    Set LED power via exponentialfunction:
     this looks more linear to human eyes
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
        # Do the calculation: the power function returns 1 when level is 0
        #  so we increase the range by 1, then subtract 1 from the result.
        pwm = ((self.max_pwm + 1) ** (level / self.max_level)) - 1
        # Write the value
        self.pin.write_analog(pwm)

    def off(self):
        self.pin.write_analog(0)

# Initialise pins etc
# Values here are good for AliExpress G90 servos @5V
svX = Servo(pin0, freq=50, min_us=700, max_us=2500, angle=180)
svY = Servo(pin1, freq=50, min_us=700, max_us=2500, angle=180)
laser = LinearLed(pin2)

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
def Laserflash(speed=1):  # Flash the laser
    for x in range(-100, 200, 2):
        laser.set_level(x)
        sleep(speed)
    for x in range(200, -100, -2):
        laser.set_level(x)
        sleep(speed)

def Demo1():  # Demo #1, draw crosses
    display.show(Image.NO)  # in this context, 'NO' is a big 'X'
    svX.write_angle(min_x)
    svY.write_angle(min_y)
    laser.off()
    sleep(1000)
    for x in range(min_x, max_x, 1):
        svX.write_angle(x)
        svY.write_angle(x/1.4)
        laser.set_level(100*(x-min_x)/(max_x-min_x))
        sleep(30)
    sleep(1000)
    svX.write_angle(max_x)
    svY.write_angle(min_y)
    laser.off()
    for x in range(min_x, max_x, 1):
        svX.write_angle(max_x-x)
        svY.write_angle(x/1.4)
        laser.set_level(100*(x-min_x)/(max_x-min_x))
        sleep(30)
    sleep(1000)

def Demo2():  # Demo #2, draw a bounds box
    display.show(Image.SQUARE)
    svX.write_angle(max_x)
    svY.write_angle(max_y)
    sleep(500)
    laser.set_level(100)
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
    laser.off()

def Play(seconds=15, speed=10, led=100):
    x = center_x * 60   # X position in seconds start at center
    y = center_y * 60   # Y position in seconds start at center
    # Turn the laser on
    for i in range(0, led, 1):
        laser.set_level(i)
        sleep(5)
    display.show(Image.PITCHFORK)
    start = utime.ticks_ms()
    while utime.ticks_diff(utime.ticks_ms(), start) <= seconds * 1000:
        x = x + random.randint(-1000, 1000)
        y = y + random.randint(-800,800)
        svX.write_angle(int(x/60))
        svY.write_angle(int(y/60))
        if button_a.was_pressed() or button_b.was_pressed():
            break
        sleep(speed*30)

    # Fade the laser down
    for i in range(led, 0, -1):
        laser.set_level(i)
        sleep(20)

# Main Loop
while True:
    if button_a.was_pressed():
        # Demo1()
        Play()
        centered = False
    if button_b.was_pressed():
        Demo2()
        centered = False
    else:
        display.show(Image.DIAMOND_SMALL)
        # Turn off and center when no buttons pressed
        if not centered:
            laser.off()
            svX.write_angle(center_x)
            svY.write_angle(center_y)
            centered = True
            sleep(500)  # wait for servos to settle
            svX.disable()
            svY.disable()
        Laserflash(speed=0)  # flash on/off as fast as possible
# fin
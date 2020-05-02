# Cat EnterTainer for BBC Micro:Bit

# Hardware
# Pin0=X

from microbit import *
import utime
import random


class Servo:
    def __init__(self, pin, freq=50, min_us=600, max_us=2400, angle=180):
        self.min_us = min_us
        self.max_us = max_us
        self.us = 0
        self.freq = freq
        self.angle = angle
        self.analog_period = 20
        self.pin = pin
        analog_period = round((1 / self.freq) * 1000)  # hertz to miliseconds
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
        start = utime.ticks_ms()  # short blocking loop
        while utime.ticks_diff(utime.ticks_ms(), start) < 250:
            if not self.pin.read_digital():  # if pin is off
                break  # break out immediately
        self.pin.write_digital(0)  # turn the pin off

    def move(self, begin, end, duration):
        # Move from start to end taking duration microseconds
        # This is a blocking function for the duration of the move
        start = utime.ticks_ms()  # short blocking loop
        degrees_ms = float((end - begin) / duration)
        while utime.ticks_diff(utime.ticks_ms(), start) <= duration:
            self.write_angle(begin + (utime.ticks_diff(utime.ticks_ms(), start) * degrees_ms))
            sleep(10)

# Initialise servo
# Values here are good for AliExpress G90 servos @5V
svX = Servo(pin0, freq=50, min_us=700, max_us=2500, angle=180)

# Limits
minX = 0
maxX = 180
midX = minX + (maxX - minX) / 2

# Status
home = False

# Functions
def Home():  # Move to center and switch off
    display.show(Image.DIAMOND_SMALL)
    svX.write_angle(midX)
    sleep(500)  # wait for servo to reach target and settle
    svX.disable()


def Demo1():  # Demo #1
    display.show(Image.NO)  # in this context, 'NO' is a big 'X'
    svX.write_angle(minX)
    sleep(1000)
    for x in range(minX, maxX, 1):
        svX.write_angle(x)
        sleep(30)
    sleep(1000)
    svX.write_angle(maxX)
    for x in range(minX, maxX, 1):
        svX.write_angle(maxX - x)
        sleep(30)
    sleep(1000)

def Demo2():  # Demo #2, move between bounds
    display.show(Image.SQUARE)
    svX.write_angle(midX)
    sleep(500)
    svX.move(midX,minX,700)
    svX.move(minX,maxX,1400)
    svX.move(maxX,midX,700)

# Main Loop
while True:
    if button_a.was_pressed():
        Demo1()
        home = False
    if button_b.was_pressed():
        Demo2()
        home = False
    else:
        # Turn off and center as necesscary
        if not home:
            Home()
            home = True
        sleep(100)
# fin

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

    A simple class for controlling hobby servos.
    Args:
        pin (pin0 .. pin3): The pin where servo is connected.
        freq (int): The frequency of the signal, in hertz.
        min_us (int): The minimum signal length supported by the servo.
        max_us (int): The maximum signal length supported by the servo.
        angle (int): The angle between minimum and maximum positions.
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
        self.pin.write_digital(0)  # turn the pin off

# Initialise pins etc
svX = Servo(pin0,freq=50, min_us=680, max_us=2500, angle=180)
svY = Servo(pin1,freq=50, min_us=680, max_us=2500, angle=180)
pin2.set_analog_period(20)  # Laser PWM period

# Limits
min_x = 0
max_x = 190
min_y = 0
max_y = 125
center_x = min_x + (max_x - min_x)/2
center_y = min_y + (max_y - min_y)/2

# Status
centered = False

while True:
    if button_a.is_pressed():
        centered = False
        display.show("+")
        svX.write_angle(min_x)
        svY.write_angle(min_y)
        pin2.write_analog(0)
        sleep(2000)
        for x in range(min_x, max_x, 2):
            # from 0 to 180 in steps of 5
            # write the angle of the step (x)
            svX.write_angle(x)
            svY.write_angle(x/1.4)
            pin2.write_analog(x*5)
            sleep(100)
        sleep(1800)
    if button_b.is_pressed():
        centered = False
        pin2.write_analog(1023)
        display.show("O")
        # show maximum and minimum rotation if button
        # b pressed
        svX.write_angle(min_x)
        svY.write_angle(min_y)
        sleep(2000)
        svX.write_angle(min_x)
        svY.write_angle(max_y)
        sleep(2000)
        svX.write_angle(max_x)
        svY.write_angle(max_y)
        sleep(2000)
        svX.write_angle(max_x)
        svY.write_angle(min_y)
        sleep(2000)
        svX.write_angle(min_x)
        svY.write_angle(min_y)
        sleep(2000)
        pin2.write_analog(0)
    else:
        display.show("-")
        # Turn off and center when no buttons pressed
        if not centered:
            pin2.write_analog(0)
            svX.write_angle(center_x)
            svY.write_angle(center_y)
            centered = True
            sleep(1000)
            svX.disable()
            svY.disable()
        sleep(200)
        if int(utime.ticks_ms()/1000) % 2 == 0:
            pin2.write_analog(0)
        else:
            pin2.write_analog(1023)
#fin
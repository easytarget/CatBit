# Cat EnterTainer for BBC Micro:Bit

# Hardware
# Pin0=X
# Pin1=Y
# Pin3=Laser

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
la = LinearLed(pin2)

# Limits
minX = 0
maxX = 180
minY = 0
maxY = 125
midX = minX + (maxX - minX) / 2
midY = minY + (maxY - minY) / 2
# Light Sensor threshold (night->day) TODO
# daylight_level = 36

# Status
home = False

# Functions
def Flash(speed=1):  # Flash the laser
    for x in range(-100, 200, 2):
        la.set_level(x)
        sleep(speed)
    for x in range(200, -100, -2):
        la.set_level(x)
        sleep(speed)


def Home():  # 'Homes the turret and kills servos + laser
    display.show(Image.DIAMOND_SMALL)
    la.off()
    svX.write_angle(midX)
    svY.write_angle(midY)
    sleep(500)  # wait for servos to settle
    svX.disable()
    svY.disable()


def Demo1():  # Demo #1, draw crosses
    display.show(Image.NO)  # in this context, 'NO' is a big 'X'
    svX.write_angle(minX)
    svY.write_angle(minY)
    la.off()
    sleep(1000)
    for x in range(minX, maxX, 1):
        svX.write_angle(x)
        svY.write_angle(x / 1.4)
        la.set_level(100 * (x - minX) / (maxX - minX))
        sleep(30)
    sleep(1000)
    svX.write_angle(maxX)
    svY.write_angle(minY)
    la.off()
    for x in range(minX, maxX, 1):
        svX.write_angle(maxX - x)
        svY.write_angle(x / 1.4)
        la.set_level(100 * (x - minX) / (maxX - minX))
        sleep(30)
    sleep(1000)

def Demo2():  # Demo #2, draw a bounds box
    display.show(Image.SQUARE)
    svX.write_angle(midX)
    svY.write_angle(maxY)
    sleep(500)
    la.set_level(100)
    svX.move(midX,minX,700)
    svY.move(maxY,minY,1400)
    svX.move(minX,maxX,1400)
    svY.move(minY,maxY,1400)
    svX.move(maxX,midX,700)
    la.off()

def Play(duration=45, speed=250, led=100):
    # Angles are expressed as seconds (degrees*60)
    x = midX * 60  # X position, start at center
    y = midY * 60  # Y position, start at center
    # Turn the laser on
    display.show(Image.TARGET)
    for i in range(0, led, 1):
        la.set_level(i)
        sleep(5)
    start = utime.ticks_ms()
    while utime.ticks_diff(utime.ticks_ms(), start) <= duration * 1000:
        # Calculate a random offset to move
        deltaX = random.randint(-1000, 1000)
        deltaY = random.randint(-800, 800)
        # Bounce off the play area edges
        if (x + deltaX > maxX * 60) or (x + deltaX < minX * 60):
            deltaX = -deltaX
        if (y + deltaY > maxY * 60) or (y + deltaY < minY * 60):
            deltaY = -deltaY
        # Set new position and move
        x = x + deltaX
        y = y + deltaY
        svX.write_angle(int(x / 60))
        svY.write_angle(int(y / 60))
        # Stop if either button pressed
        if button_a.was_pressed() or button_b.was_pressed():
            break
        # Random pause based on the requested speed
        sleep(random.randint(0, speed * 3))

    # Fade the laser down
    for i in range(led, 0, -1):
        la.set_level(i)
        sleep(20)

# Main Loop
while True:
    if button_a.was_pressed():
        # Demo1()
        Play()
        home = False
    if button_b.was_pressed():
        Demo2()
        home = False
    else:
        # Turn off and center as necesscary
        if not home:
            Home()
            home = True
        Flash(speed=0)  # flash on/off as fast as possible
# fin

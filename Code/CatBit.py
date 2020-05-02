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
        # Allow pin to settle (avoids spurious movement)
        self.pin.write_analog(0)  # pwm zero
        start = utime.ticks_ms()  # short blocking loop
        while utime.ticks_diff(utime.ticks_ms(), start) < 250:
            if not self.pin.read_digital():  # if pin is off
                break  # break out immediately
        self.pin.write_digital(0)  # turn the pin off

    def move(self, begin, end, duration):
        # Move from start to end taking duration microseconds
        # This is a blocking function for the duration of the move
        start = utime.ticks_ms()
        degrees_ms = float((end - begin) / duration)
        while utime.ticks_diff(utime.ticks_ms(), start) <= duration:
            self.write_angle(
                begin + (utime.ticks_diff(utime.ticks_ms(), start)
                         * degrees_ms)
            )
            sleep(10)
        self.write_angle(end)


class LinearLed:
    """
    Set LED power via exponentialfunction:
     this looks more linear to human eyes
    """

    def __init__(self, pin, max_pwm=1023, max_level=100):
        self.pin = pin
        self.max_pwm = max_pwm
        self.max_level = max_level
        self.level = 0

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
        self.level = level

    def off(self):
        self.pin.write_analog(0)

    def to(self, level, speed=1):
        if level != self.level:
            if level > self.level:
                d = 1
            else:
                d = -1
            for l in range(self.level, level, d):
                self.set_level(l)
                sleep(speed)


# Initialise pins etc
# Values here are good for AliExpress G90 servos @5V
svX = Servo(pin0, freq=50, min_us=700, max_us=2500, angle=180)
svY = Servo(pin1, freq=50, min_us=700, max_us=2500, angle=180)
la = LinearLed(pin2)

# Limits
minX = 40
maxX = 140
minY = 15
maxY = 80
midX = minX + (maxX - minX) / 2
midY = minY + (maxY - minY) / 2
# Light Sensor threshold (night->day) TODO
# daylight_level = 36


# Functions
def Flash(level=100, speed=1):  # Flash the laser
    la.to(level, speed)
    sleep(speed * 2 * level)
    la.to(0, speed)
    sleep(speed * 2 * level)


def Home():  # Kills laser and homes the turret
    la.off()
    svX.write_angle(midX)
    svY.write_angle(midY)
    sleep(500)  # wait for servos to settle


def Setup():  # Draw a bounds box
    display.show(Image.SQUARE)
    svX.write_angle(midX)
    svY.write_angle(minY)
    sleep(500)
    la.to(100)
    svX.move(midX, minX, 700)
    svY.move(minY, maxY, 1400)
    svX.move(minX, maxX, 1400)
    svY.move(maxY, minY, 1400)
    svX.move(maxX, midX, 700)
    la.to(0)


def Play(duration=45, speed=250, led=100):
    # Angles are expressed as seconds (degrees*60)
    x = midX * 60  # X position, start at center
    y = midY * 60  # Y position, start at center
    # Turn the laser on
    display.show(Image.TARGET)
    la.to(led, 5)
    start = utime.ticks_ms()
    while utime.ticks_diff(utime.ticks_ms(), start) <= duration * 1000:
        # Calculate a random offset to move
        deltaX = random.randint(-800, 800)
        deltaY = random.randint(-600, 600)
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
    la.to(0, 30)


# Init
last_play = utime.ticks_ms()
Home()
servo = True

# Main Loop
while True:
    if button_a.was_pressed():
        Play()
        last_play = utime.ticks_ms()
        servo = True
    if button_b.was_pressed():
        Setup()
        servo = True
    else:
        # Turn off and center as necesscary
        display.clear()
        display.set_pixel(2, 2, 5)
        if servo:
            # Home()
            svX.disable()
            svY.disable()
            servo = False
    Flash(level=60, speed=3)  # flash laser on/off
    if utime.ticks_diff(utime.ticks_ms(), last_play) > 6000000:
        Play(duration=100, speed=250)
        last_play = utime.ticks_ms()
        servo = True
# fin

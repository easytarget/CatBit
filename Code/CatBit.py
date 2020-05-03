# Cat EnterTainer for BBC Micro:Bit

# Hardware:
#   Pin0=X
#   Pin1=Y
#   Pin3=Laser

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


class LinearLed:
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
        # Do the calculation:
        #  NB: the power function returns 1 when 'level' is 0
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

# Play Area
minX = 30
maxX = 150
minY = 10
maxY = 60
midX = minX + (maxX - minX) / 2
midY = minY + (maxY - minY) / 2
# Light Sensor threshold (night->day) TODO
# daylight_level = 36


# Functions
def Go(x, y):  # Simple instant XY move
    svX.write_angle(x)
    svY.write_angle(y)


def Move(x1, y1, x2, y2, duration=0):
    # Move from start to end taking duration microseconds
    # This is a blocking function for the duration of the move
    # Calling with zero duration is OK; an instant move
    if duration > 0:
        start = utime.ticks_ms()
        x_per_ms = float((x2 - x1) / duration)
        y_per_ms = float((y2 - y1) / duration)
        # This is the primary movement loop
        while utime.ticks_diff(utime.ticks_ms(), start) <= duration:
            tx = x1 + (utime.ticks_diff(utime.ticks_ms(), start) * x_per_ms)
            ty = y1 + (utime.ticks_diff(utime.ticks_ms(), start) * y_per_ms)
            Go(tx, ty)
            sleep(10)  # We will recalculate position every 10ms
    Go(x2, y2)  # ensures we end up on final position


def Flash(level=100, speed=1):  # Flash the laser
    la.to(level, speed)
    sleep(speed * 2 * level)
    la.to(0, speed)
    sleep(speed * 2 * level)


def Home():  # Kills laser and homes the turret
    la.off()
    display.clear()
    svX.write_angle(midX)
    svY.write_angle(midY)
    sleep(500)  # wait for servos to settle


def Setup():  # Draw a bounds box
    display.show(Image.SQUARE)
    svX.write_angle(midX)
    svY.write_angle(minY)
    sleep(500)
    la.to(100)
    Move(midX, minY, minX, minY, 700)
    Move(minX, minY, minX, maxY, 1400)
    Move(minX, maxY, maxX, maxY, 1400)
    Move(maxX, maxY, maxX, minY, 1400)
    Move(maxX, minY, midX, minY, 700)
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
        # Calculate a random duration and offset to move
        deltaT = random.randint(1, 8) * random.randint(100, 500)
        deltaX = random.randint(-1600, 1600)
        deltaY = random.randint(-1000, 1000)
        # Bounce off the play area edges
        if (x + deltaX > maxX * 60) or (x + deltaX < minX * 60):
            deltaX = -deltaX
        if (y + deltaY > maxY * 60) or (y + deltaY < minY * 60):
            deltaY = -deltaY
        # move
        Move(x / 60, y / 60, (x + deltaX) / 60, (y + deltaY) / 60, deltaT)
        x += deltaX
        y += deltaY
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
display.show(Image.ALL_CLOCKS, loop=False, delay=66)
servo = True

# Main Loop
while True:
    if button_a.was_pressed():
        Play()
        last_play = utime.ticks_ms()
        servo = True
    elif button_b.was_pressed():
        Setup()
        servo = True
    if servo:  # Servo has moved, so re-home and stop
        Home()
        svX.disable()
        svY.disable()
        servo = False
    display.set_pixel(2, 2, 5)
    if utime.ticks_diff(utime.ticks_ms(), last_play) > 5500000:
        Flash(level=60, speed=3)  # flash laser on/off
    if utime.ticks_diff(utime.ticks_ms(), last_play) > 6000000:
        Play(duration=200, speed=250)
        last_play = utime.ticks_ms()
        servo = True
# fin

# Cat EnterTainer for BBC Micro:Bit

# Hardware:
#   Pin0=Servo X
#   Pin1=Servo Y
#   Pin3=Laser diode

from microbit import *
from ServoBit import Servo
from LinearLed import LinearLed
import utime
import random

# Initialise
# Values here are good for AliExpress G90 servos @5V
svX = Servo(pin0, freq=50, min_us=700, max_us=2500, angle=180)
svY = Servo(pin1, freq=50, min_us=700, max_us=2500, angle=180)
la = LinearLed(pin2)

# Play area and settings
minX = 30  # Sensible defaults
maxX = 150
minY = 10
maxY = 60
day = 40  # Light Sensor threshold
timed = True  # Timed play enabled
gap = 5000000  # Gap between Plays, ms


# Simple instant XY move
def Go(x, y):
    svX.write_angle(x)
    svY.write_angle(y)


# Move from start to end taking 'd' milliseconds
# This is a blocking function for the duration of the move
# Calling with zero duration is OK; an instant move
def Move(x1, y1, x2, y2, d=0):
    if d > 0:
        s = utime.ticks_ms()
        xs = float((x2 - x1) / d)  # How far we move per ms
        ys = float((y2 - y1) / d)
        # This is the primary movement loop
        #  The output from utime.ticks_diff is not a usable scalar
        #  for variable assignment; so this looks cumbersome.
        while utime.ticks_diff(utime.ticks_ms(), s) <= d:
            x = x1 + (utime.ticks_diff(utime.ticks_ms(), s) * xs)
            y = y1 + (utime.ticks_diff(utime.ticks_ms(), s) * ys)
            Go(x, y)
            sleep(10)
    Go(x2, y2)  # Ensure we end up on-target (fast moves)

# Display progress as a grid that lights up
def Progress(s, d):
    p = int(utime.ticks_diff(utime.ticks_ms(), s) / d * 25) % 25
    for c in range(5):
        for r in range(5):
            if c * 5 + r < p:
                display.set_pixel(c, 4 - r, pb)
            elif c * 5 + r == p:
                display.set_pixel(c, 4 - r, int(fc / 3) % (pb + 1))
            else:
                display.set_pixel(c, 4 - r, 0)


def Home():  # Kills laser and homes the turret
    la.off()
    display.clear()
    svX.write_angle(midX)
    svY.write_angle(midY)
    sleep(500)  # wait while moving
    svY.disable()
    svX.disable()


def Mode():  # Toggle timer mode, draw a play area box
    global timed
    for i in range(3): # animate a short spinner
        display.show(Image.ALL_CLOCKS, delay=33)
    display.show(Image.CLOCK12)
    sleep(330)
    if button_b.was_pressed(): # button was pressed again
        display.show(Image.SQUARE)
        svX.write_angle(midX)
        svY.write_angle(minY)
        la.to(lb, 10)
        Move(midX, minY, minX, minY, 700)
        Move(minX, minY, minX, maxY, 1400)
        Move(minX, maxY, maxX, maxY, 1400)
        Move(maxX, maxY, maxX, minY, 1400)
        Move(maxX, minY, midX, minY, 700)
        la.to(0)
    else:
        timed = not timed


def Play(duration=15, led=100):
    # Angles are expressed as seconds (degrees*60)
    x = midX * 60  # X position, start at center
    y = midY * 60  # Y position, start at center
    duration *= 1000
    # Turn the laser on
    la.to(led, 5)
    start = utime.ticks_ms()
    while utime.ticks_diff(utime.ticks_ms(), start) <= duration:
        Progress(start, duration)
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
            display.show(Image.NO)
            break
        # Random pause based on the requested speed
        sleep(random.randint(0, 600))
    # Fade the laser down
    la.to(0, 30)


# Init
last = 0
sleep(330)
servo = True
midX = minX + (maxX - minX) / 2
midY = minY + (maxY - minY) / 2
pb = 3
lb = 10
fc = 0

# Start animation
display.show(Image.ALL_ARROWS, delay=66)
display.show(Image.ARROW_N)

# Main Loop
while True:
    if servo:  # Servo has moved, go home
        Home()
        servo = False
    if button_a.was_pressed():  # Manual playtime
        Play(90, lb)
        last = utime.ticks_ms()
        servo = True
    elif button_b.was_pressed():  # Timer control and play area display
        Mode()
        servo = True
    if timed:  # Do this when timer enabled
        Progress(last, gap)
        if utime.ticks_diff(utime.ticks_ms(), last) > gap:
            Play(180, lb)
            last = utime.ticks_ms()
            servo = True
    else:
        display.set_pixel(2, 2, pb)
    # Check light level every time flashcounter rolls over
    if fc == 0:
        if display.read_light_level() > day:
            pb = 9
            lb = 100
        else:
            pb = 5
            lb = 66
    # Increment our flashcounter;
    #  rollover value changes when dimmed, to prevent visual glitches
    fc += 1
    fc %= (pb + 1) * 30
    # Spend most of our time asleep;
    #  wake up more frequently when dimmed, this keeps flash rate constant
    sleep(50 + 10 * (9 - pb))
# fin

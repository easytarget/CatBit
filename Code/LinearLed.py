import utime


class LinearLed:
    def __init__(self, pin, max_pwm=1023, max_level=100):
        self.pin = pin
        self.max_pwm = max_pwm
        self.max_level = max_level
        self.level = 0

    def set_level(self, level=0):
        # limit to range
        level = max(0, min(level, self.max_level))
        # Do the calculation:
        #  NB: the power function returns 1 when 'level' is 0
        pwm = ((self.max_pwm + 1) ** (level / self.max_level)) - 1
        # Write the value
        self.pin.write_analog(pwm)
        self.level = level

    def off(self):
        self.pin.write_analog(0)

    def on(self):
        self.set_level(self.level)

    def to(self, level, speed=1):
        if level != self.level:
            d = 1
            if level < self.level:
                d = -1
            for l in range(self.level, level, d):
                self.set_level(l)
                start = utime.ticks_ms()  # Delay loop
                while utime.ticks_diff(utime.ticks_ms(), start) <= speed:
                    pass

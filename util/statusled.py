from machine import Pin, Timer


class StatusLed:
    def __init__(self):
        self.led = Pin("LED", Pin.OUT)
        self.timer = Timer()

    def blink(self, freq):
        self.off()
        def tick(timer):
            self.led.toggle()
        self.timer.init(freq=freq, mode=Timer.PERIODIC, callback=tick)

    def tick(self):
        self.off()
        self.led.on()

        def turnLedOff(timer):
            self.led.off()
        self.timer.init(period=500, mode=Timer.ONE_SHOT, callback=turnLedOff)

    def off(self):
        self.timer.deinit()
        self.led.off()

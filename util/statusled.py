from machine import Pin, Timer


class StatusLed:
    def __init__(self):
        self.led = Pin("LED", Pin.OUT)
        self.timer = Timer()

    def blink(self, freq):
        self.off()
        self.timer.init(
            freq=freq,
            mode=Timer.PERIODIC,
            callback=lambda t: self.led.toggle()
        )

    def tick(self):
        self.off()
        self.led.on()
        self.timer.init(
            period=500,
            mode=Timer.ONE_SHOT,
            callback=lambda t: self.led.off()
        )

    def off(self):
        self.timer.deinit()
        self.led.off()

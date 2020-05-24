from time import sleep

import neopixel

from config import Config
from util import *


class RGBController:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(Config.GPIO, Config.LENGTH, brightness=Config.BRIGHTNESS,
                                        auto_write=Config.AUTO_WRITE, pixel_order=Config.ORDER)

    def __del__(self):
        self.pixels.deinit()

    def rainbow(self, wait_ms=0):
        """Whole rainbow moves across the strip."""
        while True:
            for j in range(255):
                for i in range(Config.LENGTH):
                    pixel_index = (i * 256 // Config.LENGTH) + j
                    self.pixels[i] = rainbow_wheel(pixel_index & 255)
                self.pixels.show()
                sleep(wait_ms / 1000.0)

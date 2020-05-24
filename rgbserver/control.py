import itertools
from time import sleep
from typing import Tuple

import neopixel

from config import Config
from util import *


class RGBController:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(Config.GPIO, Config.LENGTH, brightness=Config.BRIGHTNESS,
                                        auto_write=Config.AUTO_WRITE, pixel_order=Config.ORDER)

    def __del__(self):
        self.pixels.deinit()

    def rainbow(self, wait_ms: int = 0):
        """Whole rainbow moves across the strip."""
        while True:
            for j in range(255):
                for i in range(Config.LENGTH):
                    pixel_index = (i * 256 // Config.LENGTH) + j
                    self.pixels[i] = rainbow_wheel(pixel_index & 255)
                self.pixels.show()
                sleep(wait_ms / 1000.0)

    def rainbow_color_wipe(self):
        """Wipe 12 colors across display a pixel at a time."""
        for color in itertools.cycle(RAINBOW):
            self.color_wipe(color, 10)

    def color_wipe(self, color: Tuple[int, int, int], wait_ms: int = 0):
        """Wipe color across display a pixel at a time."""
        for i in range(Config.LENGTH):
            self.pixels[i] = color
            self.pixels.show()
            sleep(wait_ms / 1000.0)
